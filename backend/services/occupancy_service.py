from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from core.base_agent import BaseAgentService

class OccupancyService(BaseAgentService):

    agent_name = "occupancy"

    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data" / "occupancy_data.csv"

    def get_summary(self):
        try:
            df = pd.read_csv(self.data_path, index_col=0)

            total_records = len(df)
            occupied_records = int(df["Occupancy"].sum())
            vacant_records = total_records - occupied_records

            occupancy_rate_pct = round(
                (occupied_records / total_records) * 100, 2
            )

            occupied_df = df[df["Occupancy"] == 1]
            vacant_df = df[df["Occupancy"] == 0]

            summary = {
                "total_records": total_records,
                "occupied_records": occupied_records,
                "vacant_records": vacant_records,
                "occupancy_rate_pct": occupancy_rate_pct,
                "average_co2_when_occupied": round(occupied_df["CO2"].mean(), 2),
                "average_co2_when_vacant": round(vacant_df["CO2"].mean(), 2),
                "average_light_when_occupied": round(occupied_df["Light"].mean(), 2),
                "peak_co2_level": round(df["CO2"].max(), 2),
            }

            return self.build_response(
                status="success",
                message="Occupancy analytics generated successfully.",
                summary=summary
            )

        except Exception as e:
            return self.build_response(
                status="error",
                message=str(e),
                summary={}
            )
    FEATURES = ["Temperature", "Humidity", "Light", "CO2", "HumidityRatio"]

    def get_forecast_accuracy(self):
        try:
            data_dir = self.data_path.parent

            train_df = pd.read_csv(data_dir / "occupancy_data.csv", index_col=0)
            test1_df = pd.read_csv(data_dir / "occupancy_test1.csv", index_col=0)
            test2_df = pd.read_csv(data_dir / "occupancy_test2.csv", index_col=0)

            # Combine both real held-out test sets for a larger, genuine test sample
            test_df = pd.concat([test1_df, test2_df], ignore_index=True)

            X_train = train_df[self.FEATURES]
            y_train = train_df["Occupancy"]

            X_test = test_df[self.FEATURES]
            y_test = test_df["Occupancy"]

            model = LogisticRegression(max_iter=1000)
            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            accuracy_pct = round(accuracy_score(y_test, predictions) * 100, 2)
            precision_pct = round(precision_score(y_test, predictions) * 100, 2)
            recall_pct = round(recall_score(y_test, predictions) * 100, 2)

            summary = {
                "method": "Logistic Regression classifier (Temperature, Humidity, Light, CO2, HumidityRatio) predicting Occupancy",
                "validation_method": "Evaluated on the dataset's original real held-out test files (datatest.txt + datatest2.txt) — genuine labeled ground truth, no synthetic data used",
                "training_records": len(train_df),
                "test_records": len(test_df),
                "accuracy_pct": accuracy_pct,
                "precision_pct": precision_pct,
                "recall_pct": recall_pct,
            }

            return self.build_response(
                status="success",
                message="Occupancy forecasting model evaluated successfully.",
                summary=summary
            )

        except Exception as e:
            return self.build_response(
                status="error",
                message=str(e),
                summary={}
            )
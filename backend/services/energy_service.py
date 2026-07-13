from pathlib import Path
import pandas as pd
from core.base_agent import BaseAgentService


class EnergyService(BaseAgentService):

    agent_name = "energy"

    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data" / "train.csv"

    def get_summary(self):
        try:
            df = pd.read_csv(self.data_path, nrows=200000)

            # -------------------------------
            # Basic KPIs
            # -------------------------------
            total_records = len(df)
            total_buildings = df["building_id"].nunique()
            average_meter = round(df["meter_reading"].mean(), 2)
            maximum_meter = round(df["meter_reading"].max(), 2)
            minimum_meter = round(df["meter_reading"].min(), 2)

            # -------------------------------
            # Derived Analytics
            # -------------------------------

            half = len(df) // 2

            first_half_avg = df.iloc[:half]["meter_reading"].mean()
            second_half_avg = df.iloc[half:]["meter_reading"].mean()

            if first_half_avg > 0:
                energy_savings = (
                    (first_half_avg - second_half_avg)
                    / first_half_avg
                ) * 100
            else:
                energy_savings = 0

            energy_savings = round(energy_savings, 2)

            # Assume electricity cost = ₹8 per unit
            tariff = 8

            energy_saved_units = max(
                first_half_avg - second_half_avg,
                0
            )

            cost_savings = round(
                energy_saved_units * tariff,
                2
            )

            # -------------------------------
            # Forecast Accuracy
            # Simple baseline prediction
            # -------------------------------

            prediction = average_meter

            actual = df["meter_reading"]

            actual = actual.replace(0, 0.0001)

            mape = (
                abs(actual - prediction) / actual
            ).mean() * 100

            forecast_accuracy = round(
                max(0, 100 - mape),
                2
            )

            summary = {

                "total_records": total_records,

                "total_buildings": total_buildings,

                "average_meter_reading": average_meter,

                "maximum_meter_reading": maximum_meter,

                "minimum_meter_reading": minimum_meter,

                "energy_savings": energy_savings,

                "cost_savings": cost_savings,

                "forecast_accuracy": forecast_accuracy,

            }

            return self.build_response(
                status="success",
                message="Energy analytics generated successfully.",
                summary=summary,
                extra={
                    "dataset": {
                        "columns": list(df.columns)
                    }
                }
            )

        except Exception as e:
            return self.build_response(
                status="error",
                message=str(e),
                summary={}
            )
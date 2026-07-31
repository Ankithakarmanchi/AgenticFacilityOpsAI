import os
import pandas as pd
from core.base_agent import BaseAgentService


class MaintenanceService(BaseAgentService):

    agent_name = "maintenance"

    def __init__(self):
        data_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "maintenance_assets.csv"
        )

        self.df = pd.read_csv(data_path)

    def calculate_health_score(self, row):
        score = 100

        score -= max(0, row["Tool wear [min]"] / 5)
        score -= max(0, (row["Air temperature [K]"] - 298) * 2)
        score -= max(0, (row["Process temperature [K]"] - 308) * 2)

        if row["Rotational speed [rpm]"] < 1400:
            score -= 10

        if row["Torque [Nm]"] > 60:
            score -= 15

        return max(0, round(score, 1))

    def classify_asset(self, score):
        if score >= 85:
            return "Healthy"
        elif score >= 60:
            return "Warning"
        else:
            return "Critical"

    def get_summary(self):

        df = self.df.copy()

        df["Health Score"] = df.apply(
            self.calculate_health_score,
            axis=1
        )

        df["Status"] = df["Health Score"].apply(
            self.classify_asset
        )

        summary = {
            "total_assets": len(df),
            "healthy_assets": len(df[df["Status"] == "Healthy"]),
            "warning_assets": len(df[df["Status"] == "Warning"]),
            "critical_assets": len(df[df["Status"] == "Critical"]),
            "average_health_score": round(
                df["Health Score"].mean(),
                2
            )
        }

        return self.build_response(
            status="success",
            message="Maintenance analytics generated successfully.",
            summary=summary
        )

    def get_alerts(self):

        df = self.df.copy()

        df["Health Score"] = df.apply(
            self.calculate_health_score,
            axis=1
        )

        df["Status"] = df["Health Score"].apply(
            self.classify_asset
        )

        critical = df[df["Status"] == "Critical"]

        alerts = []

        asset_types = {
            "L": "HVAC Unit",
            "M": "Pump",
            "H": "Chiller"
        }

        for index, (_, row) in enumerate(
            critical.sort_values("Health Score").head(10).iterrows(),
            start=1
        ):

            asset_name = f"{asset_types.get(row['Type'], 'Asset')}-{index:02d}"

            alerts.append({
                "asset": asset_name,
                "product_id": row["Product ID"],
                "health_score": row["Health Score"],
                "failure": bool(row["Machine failure"]),
                "message": "Immediate inspection recommended."
            })

        return alerts

    def get_recommendations(self):

        df = self.df.copy()

        df["Health Score"] = df.apply(
            self.calculate_health_score,
            axis=1
        )

        asset_types = {
            "L": "HVAC Unit",
            "M": "Pump",
            "H": "Chiller"
        }

        recommendations = []

        for index, (_, row) in enumerate(
            df.sort_values("Health Score").head(10).iterrows(),
            start=1
        ):

            asset_name = f"{asset_types.get(row['Type'], 'Asset')}-{index:02d}"

            if row["Health Score"] < 50:
                priority = "High"
                action = "Schedule maintenance immediately."
            elif row["Health Score"] < 70:
                priority = "Medium"
                action = "Inspect within the next 7 days."
            else:
                priority = "Low"
                action = "Continue routine monitoring."

            recommendations.append({
                "asset": asset_name,
                "health_score": row["Health Score"],
                "priority": priority,
                "action": action
            })

        return recommendations
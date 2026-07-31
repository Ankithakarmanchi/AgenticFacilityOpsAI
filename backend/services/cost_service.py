from pathlib import Path
import pandas as pd
from core.base_agent import BaseAgentService


class CostService(BaseAgentService):

    agent_name = "cost"

    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data" / "cost_data.csv"

    def _load_data(self):
        df = pd.read_csv(self.data_path, sep=None, engine="python")
        df.columns = df.columns.str.strip()
        return df

    def get_summary(self):
        try:
            df = self._load_data()

            total_amount = float(df["Amount"].sum())
            total_budget = float(df["Budget_Allocated"].sum())
            total_variance = float(df["Variance"].sum())

            category_breakdown = (
                df.groupby("Category")["Amount"].sum().round(2).to_dict()
            )

            status_breakdown = df["Status"].value_counts().to_dict()
            priority_breakdown = df["Priority"].value_counts().to_dict()

            summary = {
                "total_reports": len(df),
                "buildings_covered": int(df["Building"].nunique()),
                "vendors_engaged": int(df["Vendor"].nunique()),
                "total_amount_spent": round(total_amount, 2),
                "total_budget_allocated": round(total_budget, 2),
                "total_variance": round(total_variance, 2),
                "over_budget_reports": int(status_breakdown.get("Over Budget", 0)),
                "under_budget_reports": int(status_breakdown.get("Under Budget", 0)),
                "category_breakdown": category_breakdown,
                "priority_breakdown": priority_breakdown,
            }

            return self.build_response(
                status="success",
                message="Cost analytics generated successfully.",
                summary=summary
            )

        except Exception as e:
            return self.build_response(
                status="error",
                message=str(e),
                summary={}
            )

    def get_recommendations(self):
        try:
            df = self._load_data()

            over_budget = df[df["Status"] == "Over Budget"].sort_values(
                "Variance", ascending=False
            )

            recommendations = []

            for _, row in over_budget.head(10).iterrows():
                recommendations.append({
                    "report_id": row["Report_ID"],
                    "building": row["Building"],
                    "category": row["Category"],
                    "vendor": row["Vendor"],
                    "variance": row["Variance"],
                    "priority": row["Priority"],
                    "action": f"Review {row['Vendor']} contract for {row['Category']} at {row['Building']} — exceeded budget by {row['Variance']}."
                })

            return recommendations

        except Exception as e:
            return [{"error": str(e)}]
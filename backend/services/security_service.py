from pathlib import Path
import pandas as pd
from core.base_agent import BaseAgentService


class SecurityService(BaseAgentService):

    agent_name = "security"

    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data" / "security_data.csv"

    def _load_data(self):
        # sep=None + engine="python" auto-detects tab vs comma delimiter
        df = pd.read_csv(self.data_path, sep=None, engine="python")
        df.columns = df.columns.str.strip()
        return df

    def get_summary(self):
        try:
            df = self._load_data()

            total_events = len(df)

            access_result_breakdown = df["Access_Result"].value_counts().to_dict()
            severity_breakdown = df["Severity"].value_counts().to_dict()
            event_type_breakdown = df["Event"].value_counts().to_dict()

            denied_count = int(
                df[df["Access_Result"].str.strip().str.lower() != "granted"].shape[0]
            )

            summary = {
                "total_events": total_events,
                "buildings_monitored": int(df["Building"].nunique()),
                "unique_employees": int(df["Employee_ID"].nunique()),
                "unauthorized_attempts": denied_count,
                "access_result_breakdown": access_result_breakdown,
                "severity_breakdown": severity_breakdown,
                "event_type_breakdown": event_type_breakdown,
            }

            return self.build_response(
                status="success",
                message="Security analytics generated successfully.",
                summary=summary
            )

        except Exception as e:
            return self.build_response(
                status="error",
                message=str(e),
                summary={}
            )

    def get_alerts(self):
        try:
            df = self._load_data()

            flagged = df[df["Access_Result"].str.strip().str.lower() != "granted"]

            alerts = []

            for _, row in flagged.head(20).iterrows():
                alerts.append({
                    "timestamp": str(row["Timestamp"]),
                    "building": row["Building"],
                    "zone": row["Zone"],
                    "door": row["Door"],
                    "employee_id": row["Employee_ID"],
                    "access_result": row["Access_Result"],
                    "severity": row["Severity"],
                    "message": "Unauthorized or denied access attempt detected."
                })

            return alerts

        except Exception as e:
            return [{"error": str(e)}]
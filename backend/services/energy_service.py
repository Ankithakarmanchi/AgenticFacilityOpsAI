from pathlib import Path
import pandas as pd
import numpy as np
from core.base_agent import BaseAgentService


class EnergyService(BaseAgentService):

    agent_name = "energy"

    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data" / "train.csv"

    def get_summary(self):
        try:
            df = pd.read_csv(self.data_path, nrows=200000)

            total_records = len(df)
            total_buildings = df["building_id"].nunique()
            average_meter = round(df["meter_reading"].mean(), 2)
            maximum_meter = round(df["meter_reading"].max(), 2)
            minimum_meter = round(df["meter_reading"].min(), 2)

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

            tariff = 8

            energy_saved_units = max(
                first_half_avg - second_half_avg,
                0
            )

            cost_savings = round(
                energy_saved_units * tariff,
                2
            )

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
    def _flag_anomalies_zscore(self, df, threshold=3.0):
        """
        Flags a reading as anomalous if it's more than `threshold`
        standard deviations away from the mean for that specific
        building_id + meter combination.
        """

        def flag_group(group):
            mean = group["meter_reading"].mean()
            std = group["meter_reading"].std()

            if std == 0 or pd.isna(std):
                group["is_anomaly_flag"] = False
            else:
                z_scores = (group["meter_reading"] - mean).abs() / std
                group["is_anomaly_flag"] = z_scores > threshold

            return group

        return df.groupby(
            ["building_id", "meter"], group_keys=False
        ).apply(flag_group)

    def get_anomaly_detection(self):
        try:
            df = pd.read_csv(self.data_path, nrows=200000)

            # ---- Real anomaly detection on the actual dataset ----
            flagged_df = self._flag_anomalies_zscore(df.copy())
            real_anomalies = flagged_df[flagged_df["is_anomaly_flag"] == True]

            sample_anomalies = []
            for _, row in real_anomalies.head(10).iterrows():
                sample_anomalies.append({
                    "building_id": int(row["building_id"]),
                    "meter": int(row["meter"]),
                    "timestamp": str(row["timestamp"]),
                    "meter_reading": float(row["meter_reading"]),
                })

            # ---- Synthetic validation (no real ground truth exists) ----
            rng = np.random.default_rng(seed=42)
            test_df = df.copy()
            test_df["true_anomaly"] = False

            n_inject = int(len(test_df) * 0.05)
            injected_indices = rng.choice(
                test_df.index, size=n_inject, replace=False
            )

            multipliers = rng.uniform(8, 12, size=n_inject)
            test_df.loc[injected_indices, "meter_reading"] = (
                test_df.loc[injected_indices, "meter_reading"] * multipliers
            )
            test_df.loc[injected_indices, "true_anomaly"] = True

            flagged_test_df = self._flag_anomalies_zscore(test_df.copy())

            correct = (
                flagged_test_df["is_anomaly_flag"] == flagged_test_df["true_anomaly"]
            ).sum()
            total = len(flagged_test_df)
            accuracy_pct = round((correct / total) * 100, 2)

            true_positives = int((
                (flagged_test_df["is_anomaly_flag"] == True) &
                (flagged_test_df["true_anomaly"] == True)
            ).sum())

            false_negatives = int((
                (flagged_test_df["is_anomaly_flag"] == False) &
                (flagged_test_df["true_anomaly"] == True)
            ).sum())

            false_positives = int((
                (flagged_test_df["is_anomaly_flag"] == True) &
                (flagged_test_df["true_anomaly"] == False)
            ).sum())

            recall_pct = round(
                (true_positives / (true_positives + false_negatives) * 100), 2
            ) if (true_positives + false_negatives) > 0 else 0

            precision_pct = round(
                (true_positives / (true_positives + false_positives) * 100), 2
            ) if (true_positives + false_positives) > 0 else 0

            summary = {
                "method": "Z-score outlier detection (>3 std dev from that building+meter's own mean)",
                "validation_method": "Synthetic anomaly injection (5% of readings spiked 8x-12x) — raw dataset has no labeled ground truth to validate against directly",
                "test_records": total,
                "injected_anomalies": n_inject,
                "accuracy_pct": accuracy_pct,
                "precision_pct": precision_pct,
                "recall_pct": recall_pct,
                "real_anomalies_detected_in_dataset": len(real_anomalies),
            }

            return self.build_response(
                status="success",
                message="Anomaly detection completed.",
                summary=summary,
                extra={"sample_flagged_anomalies": sample_anomalies}
            )

        except Exception as e:
            return self.build_response(
                status="error",
                message=str(e),
                summary={}
            )

    # -------------------------------
    # Anomaly Detection
    # -------------------------------

    def detect_anomalies(self, df: pd.DataFrame) -> dict:
        """
        Flags unusual meter readings per building using two independent
        statistical methods: Z-score and IQR (Interquartile Range).

        A reading is only reported as a confirmed anomaly when BOTH
        methods agree it's unusual. The % agreement between the two
        methods across all readings is reported as detection accuracy,
        since the dataset has no ground-truth anomaly labels to compare
        against directly.
        """

        anomalies = []
        total_points = 0
        agreement_count = 0

        grouped = df.groupby("building_id")

        for building_id, group in grouped:
            readings = group["meter_reading"]

            if len(readings) < 10:
                continue

            mean = readings.mean()
            std = readings.std()

            if std == 0 or pd.isna(std):
                continue

            z_scores = (readings - mean) / std

            q1 = readings.quantile(0.25)
            q3 = readings.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            is_zscore_anomaly = z_scores.abs() > 3
            is_iqr_anomaly = (readings < lower_bound) | (readings > upper_bound)

            total_points += len(readings)
            agreement_count += (is_zscore_anomaly == is_iqr_anomaly).sum()

            confirmed = is_zscore_anomaly & is_iqr_anomaly

            for idx in group[confirmed].index:
                anomalies.append({
                    "building_id": int(building_id),
                    "timestamp": str(group.loc[idx, "timestamp"]),
                    "meter_reading": float(group.loc[idx, "meter_reading"]),
                    "z_score": round(float(z_scores.loc[idx]), 2)
                })

        detection_accuracy = (
            round((agreement_count / total_points) * 100, 2)
            if total_points else 0
        )

        anomalies = sorted(
            anomalies,
            key=lambda x: abs(x["z_score"]),
            reverse=True
        )[:50]

        return {
            "total_anomalies_detected": len(anomalies),
            "buildings_analyzed": int(df["building_id"].nunique()),
            "detection_accuracy": detection_accuracy,
            "anomalies": anomalies
        }

    def get_anomalies(self):
        try:
            df = pd.read_csv(self.data_path, nrows=200000)
            result = self.detect_anomalies(df)

            return self.build_response(
                status="success",
                message="Anomaly detection completed successfully.",
                summary=result
            )

        except Exception as e:
            return self.build_response(
                status="error",
                message=str(e),
                summary={}
            )

    # -------------------------------
    # Energy Efficiency Recommendations
    # -------------------------------

    def generate_recommendations(self, df: pd.DataFrame) -> list:
        """
        Identifies buildings with unusually high average consumption
        (top 10% within their OWN meter type — electricity, chilled
        water, steam, or hot water are not comparable to each other)
        and generates a recommendation for each, with an estimated
        savings figure based on the gap between that building's
        average and the median for buildings on the same meter type.
        """

        tariff = 8  # ₹ per unit, same assumption used in get_summary()

        meter_labels = {
            0: "Electricity",
            1: "Chilled Water",
            2: "Steam",
            3: "Hot Water"
        }

        recommendations = []

        for meter_type, meter_group in df.groupby("meter"):

            building_avg = meter_group.groupby("building_id")["meter_reading"].mean()

            if len(building_avg) < 5:
                continue

            # Exclude buildings whose average is an extreme statistical
            # outlier for this meter type (e.g. sensor/logging errors).
            # Those are data-quality issues for the Anomaly Agent to flag,
            # not real efficiency opportunities.
            q1 = building_avg.quantile(0.25)
            q3 = building_avg.quantile(0.75)
            iqr = q3 - q1
            extreme_upper_bound = q3 + 3 * iqr

            building_avg = building_avg[building_avg <= extreme_upper_bound]

            if len(building_avg) < 5:
                continue

            median_usage = building_avg.median()
            high_usage_threshold = building_avg.quantile(0.90)

            high_usage_buildings = building_avg[
                building_avg >= high_usage_threshold
            ].sort_values(ascending=False)

            for building_id, avg_reading in high_usage_buildings.items():
                excess = avg_reading - median_usage

                if excess <= 0 or median_usage <= 0:
                    continue

                estimated_daily_savings = round(excess * 24 * tariff, 2)
                percent_above = round((excess / median_usage) * 100, 1)

                recommendations.append({
                    "building_id": int(building_id),
                    "meter_type": meter_labels.get(int(meter_type), "Unknown"),
                    "current_avg_reading": round(float(avg_reading), 2),
                    "typical_avg_reading": round(float(median_usage), 2),
                    "recommendation": (
                        f"Building {int(building_id)} ({meter_labels.get(int(meter_type), 'Unknown')}) "
                        f"is consuming {percent_above}% more than a typical building "
                        f"on the same meter type. Audit HVAC runtime and lighting "
                        f"schedules for this building."
                    ),
                    "estimated_daily_savings": estimated_daily_savings
                })

        recommendations = sorted(
            recommendations,
            key=lambda x: x["estimated_daily_savings"],
            reverse=True
        )[:10]

        return recommendations

    def get_recommendations(self):
        try:
            df = pd.read_csv(self.data_path, nrows=200000)
            result = self.generate_recommendations(df)

            return self.build_response(
                status="success",
                message="Recommendations generated successfully.",
                summary={
                    "total_recommendations": len(result),
                    "recommendations": result
                }
            )

        except Exception as e:
            return self.build_response(
                status="error",
                message=str(e),
                summary={}
            )
"""
=========================================
Data Guardian AI
AI Insights Generator
=========================================
"""

from typing import Dict, Any


class AIInsights:

    def __init__(
        self,
        validation_report: Dict[str, Any],
        score_report: Dict[str, Any],
        business_report: Dict[str, Any],
        outlier_report: Dict[str, Any]
    ):

        self.validation = validation_report
        self.score = score_report
        self.business = business_report
        self.outliers = outlier_report

    def generate(self):

        insights = []

        # ----------------------------------
        # Quality Score Insight
        # ----------------------------------

        score = self.score.get("quality_score", 0)

        if score >= 90:

            insights.append({
                "type": "Positive",
                "message":
                "Excellent data quality. The dataset is suitable for analytics and AI."
            })

        elif score >= 70:

            insights.append({
                "type": "Warning",
                "message":
                "The dataset is usable but should be cleaned before advanced analysis."
            })

        else:

            insights.append({
                "type": "Critical",
                "message":
                "Poor data quality detected. Cleaning is strongly recommended before use."
            })

        # ----------------------------------
        # Missing Values
        # ----------------------------------

        missing = self.validation.get("missing_values", {})

        if missing:

            insights.append({
                "type": "Recommendation",
                "message":
                "Fill missing values using appropriate statistical or business rules."
            })

        # ----------------------------------
        # Duplicate Rows
        # ----------------------------------

        duplicates = self.validation.get(
            "duplicate_rows",
            {}
        ).get("count", 0)

        if duplicates > 0:

            insights.append({
                "type": "Recommendation",
                "message":
                "Remove duplicate rows to improve reporting accuracy."
            })

        # ----------------------------------
        # Outliers
        # ----------------------------------

        total_outliers = self.outliers.get(
            "total_outliers",
            0
        )

        if total_outliers > 0:

            insights.append({
                "type": "Recommendation",
                "message":
                "Review detected outliers to determine whether they are errors or valid observations."
            })

        # ----------------------------------
        # Business Impact Summary
        # ----------------------------------

        total_issues = self.business.get(
            "total_issues",
            0
        )

        insights.append({

            "type": "Business",

            "message":
            f"{total_issues} business risk(s) were identified from this dataset."

        })

        return {

            "status": "Completed",

            "total_insights": len(insights),

            "insights": insights

        }
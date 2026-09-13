from typing import Dict, Any


class DataQualityScorer:
    """
    Calculates an overall data quality score.
    """

    def __init__(
        self,
        validation_result: Dict[str, Any],
        outlier_result: Dict[str, Any],
    ):
        self.validation = validation_result
        self.outliers = outlier_result

    def calculate_score(self):

        score = 100

        # -----------------------------
        # Missing Values
        # -----------------------------

        missing_values = self.validation.get(
            "missing_values",
            {}
        )

        total_missing = sum(

            value["count"]

            for value in missing_values.values()

        )

        score -= total_missing * 2

        # -----------------------------
        # Duplicate Rows
        # -----------------------------

        duplicate_rows = self.validation.get(
            "duplicate_rows",
            {}
        ).get("count", 0)

        score -= duplicate_rows * 3

        # -----------------------------
        # Empty Columns
        # -----------------------------

        empty_columns = len(

            self.validation.get(

                "empty_columns",

                []

            )

        )

        score -= empty_columns * 5

        # -----------------------------
        # Outliers
        # -----------------------------

        total_outliers = self.outliers.get(

            "total_outliers",

            0

        )

        score -= total_outliers

        # -----------------------------
        # Clamp Score
        # -----------------------------

        score = max(0, min(100, score))

        # -----------------------------
        # Grade
        # -----------------------------

        if score >= 90:
            grade = "Excellent"

        elif score >= 75:
            grade = "Good"

        elif score >= 60:
            grade = "Fair"

        elif score >= 40:
            grade = "Poor"

        else:
            grade = "Critical"

        # -----------------------------
        # Return Standard Format
        # -----------------------------

        return {

            "quality_score": score,

            "grade": grade,

            "status": "Completed",

            "summary": {

                "missing_values": total_missing,

                "duplicate_rows": duplicate_rows,

                "empty_columns": empty_columns,

                "total_outliers": total_outliers

            }

        }
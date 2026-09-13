

from typing import Dict, Any


class BusinessImpactAnalyzer:

    def __init__(
        self,
        validation_result: Dict[str, Any],
        outlier_result: Dict[str, Any]
    ):

        self.validation = validation_result
        self.outliers = outlier_result

    def analyse(self):

        impacts = []

        # -----------------------------------
        # Missing Values
        # -----------------------------------

        missing = self.validation.get(
            "missing_values",
            {}
        )

        total_missing = sum(

            item["count"]

            for item in missing.values()

        )

        if total_missing > 0:

            impacts.append({

                "issue": "Missing Values",

                "severity": "Medium",

                "impact":
                "Incomplete records can reduce reporting accuracy and affect decision-making.",

                "recommendation":
                "Fill or estimate missing values before using the dataset."

            })

        # -----------------------------------
        # Duplicate Rows
        # -----------------------------------

        duplicates = self.validation.get(
            "duplicate_rows",
            {}
        ).get("count", 0)

        if duplicates > 0:

            impacts.append({

                "issue": "Duplicate Rows",

                "severity": "High",

                "impact":
                "Duplicate records can inflate totals and distort business reports.",

                "recommendation":
                "Remove duplicate records before analysis."

            })

        # -----------------------------------
        # Empty Columns
        # -----------------------------------

        empty_columns = self.validation.get(
            "empty_columns",
            []
        )

        if len(empty_columns) > 0:

            impacts.append({

                "issue": "Empty Columns",

                "severity": "Low",

                "impact":
                "Unused columns increase storage and make datasets harder to maintain.",

                "recommendation":
                "Delete or populate empty columns."

            })

        # -----------------------------------
        # Outliers
        # -----------------------------------

        total_outliers = self.outliers.get(
            "total_outliers",
            0
        )

        if total_outliers > 0:

            impacts.append({

                "issue": "Outliers",

                "severity": "Medium",

                "impact":
                "Extreme values can skew averages, trends, and predictive models.",

                "recommendation":
                "Investigate whether the outliers are errors or genuine observations."

            })

        # -----------------------------------
        # Return Standard Format
        # -----------------------------------

        return {

            "status": "Completed",

            "total_issues": len(impacts),

            "business_impacts": impacts

        }
from typing import Dict, Any
from datetime import datetime


class ReportGenerator:

    def __init__(self, analysis_result: Dict[str, Any]):

        self.analysis = analysis_result


    def generate(self):

        score = self.analysis["quality_score"]

        report = {

            "title": "Data Guardian AI Executive Report",

            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "overall_quality": {

                "score": score["quality_score"],

                "grade": score["grade"]

            },

            "dataset_profile":
                self.analysis["profile"],

            "validation":
                self.analysis["validation"],

            "outliers":
                self.analysis["outliers"],

            "cleaning":
                self.analysis["cleaning"],
                    "ml_analytics": self.analysis.get(
        "ml_analytics",
         {}
),
            "visualizations": self.analysis.get(
    "visualizations",
    {}
), 

            "business_impact":
                self.analysis["business_impact"],

            "ai_insights":
                self.analysis["ai_insights"],

            "executive_summary":
                self.executive_summary(score)

        }

        return report

    def executive_summary(self, score):

        quality = score["quality_score"]

        if quality >= 90:

            return (
                "The dataset is of excellent quality and "
                "is ready for reporting, machine learning, "
                "and business intelligence."
            )

        elif quality >= 75:

            return (
                "The dataset is generally reliable, "
                "but minor cleaning is recommended."
            )

        elif quality >= 60:

            return (
                "The dataset contains several quality "
                "issues that should be corrected before "
                "performing advanced analytics."
            )

        else:

            return (
                "The dataset has significant quality "
                "issues. Extensive cleaning is required "
                "before it should be used."
            )
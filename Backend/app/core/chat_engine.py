"""
=========================================
Data Guardian AI
Chat Engine
=========================================
"""

from typing import Dict, Any


class ChatEngine:
    """
    Generates AI responses from the user's prompt
    and the analysis results.
    """

    def __init__(
        self,
        prompt: str,
        analysis_result: Dict[str, Any]
    ):
        self.prompt = prompt
        self.analysis = analysis_result

    def respond(self):

        prompt = self.prompt.lower()

        score = self.analysis["quality_score"]["quality_score"]
        grade = self.analysis["quality_score"]["grade"]

        validation = self.analysis["validation"]
        outliers = self.analysis["outliers"]
        business = self.analysis["business_impact"]
        insights = self.analysis["ai_insights"]

        # -------------------------
        # Quality Score
        # -------------------------

        if "score" in prompt or "quality" in prompt:

            return {
                "status": "Completed",
                "response":
                    f"The dataset quality score is {score}/100 "
                    f"with a grade of '{grade}'."
            }

        # -------------------------
        # Missing Values
        # -------------------------

        if "missing" in prompt:

            return {
                "status": "Completed",
                "response":
                    f"I found {len(validation['missing_values'])} column(s) containing missing values."
            }

        # -------------------------
        # Outliers
        # -------------------------

        if "outlier" in prompt:

            return {
                "status": "Completed",
                "response":
                    f"The analysis detected {outliers['total_outliers']} outlier(s)."
            }

        # -------------------------
        # Business Impact
        # -------------------------

        if "business" in prompt or "risk" in prompt:

            return {
                "status": "Completed",
                "response":
                    f"There are {business['total_issues']} business issue(s) identified that could affect reporting and decision-making."
            }

        # -------------------------
        # AI Insights
        # -------------------------

        if "insight" in prompt or "recommendation" in prompt:

            messages = [
                item["message"]
                for item in insights["insights"]
            ]

            return {
                "status": "Completed",
                "response": messages
            }

        # -------------------------
        # Default Response
        # -------------------------

        return {
            "status": "Completed",
            "response":
                "I can analyse datasets, explain missing values, detect outliers, calculate quality scores, generate executive reports, and provide business recommendations."
        }
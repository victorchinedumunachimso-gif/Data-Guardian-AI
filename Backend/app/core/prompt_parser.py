"""
=========================================
Data Guardian AI
Prompt Parser
=========================================
"""


class PromptParser:
    """
    Detects the user's intention from a text prompt.
    """

    def __init__(self, prompt: str):
        self.prompt = prompt.lower().strip()

    def parse(self):

        intents = []

        # Analysis
        if any(word in self.prompt for word in [
            "analyse", "analyze", "analysis"
        ]):
            intents.append("analyse")

        # Cleaning
        if any(word in self.prompt for word in [
            "clean", "fix", "repair"
        ]):
            intents.append("clean")

        # Missing Values
        if any(word in self.prompt for word in [
            "missing", "null", "empty values"
        ]):
            intents.append("missing_values")

        # Duplicate Rows
        if any(word in self.prompt for word in [
            "duplicate", "duplicates"
        ]):
            intents.append("duplicates")

        # Outliers
        if any(word in self.prompt for word in [
            "outlier", "outliers", "anomaly"
        ]):
            intents.append("outliers")

        # Quality Score
        if any(word in self.prompt for word in [
            "score", "quality", "grade"
        ]):
            intents.append("quality_score")

        # Executive Report
        if any(word in self.prompt for word in [
            "report", "summary", "executive"
        ]):
            intents.append("report")

        # Business Impact
        if any(word in self.prompt for word in [
            "business", "impact", "risk"
        ]):
            intents.append("business_impact")

        # AI Insights
        if any(word in self.prompt for word in [
            "insight", "recommendation", "advice"
        ]):
            intents.append("ai_insights")

        if not intents:
            intents.append("general")

        return {
            "status": "Completed",
            "prompt": self.prompt,
            "intents": intents
        }
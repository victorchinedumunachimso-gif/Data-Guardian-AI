"""
=========================================
Data Guardian AI
AI Orchestrator
=========================================
"""

from typing import Dict, Any

from app.core.prompt_parser import PromptParser
from app.core.chat_engine import ChatEngine
from app.core.report_generator import ReportGenerator


class AIOrchestrator:
    """
    Coordinates the AI workflow.
    """

    def __init__(
        self,
        prompt: str,
        analysis_result: Dict[str, Any]
    ):

        self.prompt = prompt
        self.analysis = analysis_result

    def execute(self):

        # ---------------------------------
        # Parse Prompt
        # ---------------------------------

        parser = PromptParser(self.prompt)

        parsed = parser.parse()

        intents = parsed["intents"]

        # ---------------------------------
        # Generate Executive Report
        # ---------------------------------

        report = None

        if "report" in intents:

            generator = ReportGenerator(
                self.analysis
            )

            report = generator.generate()

        # ---------------------------------
        # Generate AI Chat Response
        # ---------------------------------

        chat = ChatEngine(

            prompt=self.prompt,

            analysis_result=self.analysis

        )

        response = chat.respond()

        # ---------------------------------
        # Final Response
        # ---------------------------------

        return {

            "status": "Completed",

            "prompt": self.prompt,

            "intents": intents,

            "chat_response": response,

            "executive_report": report

        }
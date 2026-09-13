from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class ExecutiveReport:

    def __init__(
        self,
        filename,
        profile,
        validation,
        score,
        insights,
        cleaning
    ):

        self.filename = filename
        self.profile = profile
        self.validation = validation
        self.score = score
        self.insights = insights
        self.cleaning = cleaning

    def generate(self, output_path):

        document = SimpleDocTemplate(output_path)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>DATA GUARDIAN AI</b>",
                styles["Title"]
            )
        )

        story.append(
            Paragraph(
                "Executive Data Quality Report",
                styles["Heading1"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Dataset:</b> {self.filename}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Quality Score:</b> {self.score['quality_score']}/100",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Grade:</b> {self.score['grade']}",
                styles["BodyText"]
            )
        )

        document.build(story)

        return output_path
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


class PDFReportService:

    def __init__(self, report):
        self.report = report

    def generate(self):

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=22,
            leading=28,
            spaceAfter=12
        )

        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=15,
            leading=20,
            spaceBefore=12,
            spaceAfter=8
        )

        normal_style = ParagraphStyle(
            "ReportBody",
            parent=styles["BodyText"],
            fontSize=10,
            leading=15,
            spaceAfter=6
        )

        story = []

        # ==========================================
        # TITLE
        # ==========================================

        story.append(
            Paragraph(
                self.report.get(
                    "title",
                    "Data Guardian AI Executive Report"
                ),
                title_style
            )
        )

        story.append(
            Paragraph(
                f"Generated: {self.report.get('generated_at', '--')}",
                normal_style
            )
        )

        story.append(Spacer(1, 8))

        # ==========================================
        # OVERALL QUALITY
        # ==========================================

        story.append(
            Paragraph(
                "Overall Data Quality",
                heading_style
            )
        )

        quality = self.report.get(
            "overall_quality",
            {}
        )

        quality_table = Table([
            ["Quality Score", "Grade"],
            [
                str(
                    quality.get(
                        "score",
                        0
                    )
                ) + "%",
                quality.get(
                    "grade",
                    "Unknown"
                )
            ]
        ], colWidths=[80 * mm, 80 * mm])

        quality_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#111827")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, 1),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    11
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                )
            ])
        )

        story.append(quality_table)

        story.append(Spacer(1, 12))

        # ==========================================
        # EXECUTIVE SUMMARY
        # ==========================================

        story.append(
            Paragraph(
                "Executive Summary",
                heading_style
            )
        )

        story.append(
            Paragraph(
                self.report.get(
                    "executive_summary",
                    "No executive summary available."
                ),
                normal_style
            )
        )

        # ==========================================
        # DATASET PROFILE
        # ==========================================

        story.append(
            Paragraph(
                "Dataset Profile",
                heading_style
            )
        )

        profile = self.report.get(
            "dataset_profile",
            {}
        )

        profile_table = Table([
            ["Metric", "Value"],
            [
                "Rows",
                str(profile.get("rows", 0))
            ],
            [
                "Columns",
                str(profile.get("columns", 0))
            ],
            [
                "Memory Usage",
                f"{profile.get('memory_usage_mb', 0)} MB"
            ]
        ], colWidths=[80 * mm, 80 * mm])

        profile_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#6d00ff")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ])
        )

        story.append(profile_table)

        # ==========================================
        # VALIDATION
        # ==========================================

        story.append(
            Paragraph(
                "Validation Findings",
                heading_style
            )
        )

        validation = self.report.get(
            "validation",
            {}
        )

        missing_values = validation.get(
            "missing_values",
            {}
        )

        duplicate_rows = validation.get(
            "duplicate_rows",
            {}
        )

        empty_columns = validation.get(
            "empty_columns",
            []
        )

        validation_table = Table([
            ["Issue", "Count"],
            [
                "Columns with Missing Values",
                str(len(missing_values))
            ],
            [
                "Duplicate Rows",
                str(
                    duplicate_rows.get(
                        "count",
                        0
                    )
                )
            ],
            [
                "Empty Columns",
                str(len(empty_columns))
            ]
        ], colWidths=[100 * mm, 60 * mm])

        validation_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#111827")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ])
        )

        story.append(validation_table)

        # ==========================================
        # OUTLIERS
        # ==========================================

        story.append(
            Paragraph(
                "Outlier Analysis",
                heading_style
            )
        )

        outliers = self.report.get(
            "outliers",
            {}
        )

        outlier_rows = [
            [
                "Column",
                "Outliers",
                "Lower Limit",
                "Upper Limit"
            ]
        ]

        for column, info in (
            outliers.get("columns", {})
            .items()
        ):

            outlier_rows.append([
                column,
                str(info.get("count", 0)),
                str(info.get("lower_limit", "--")),
                str(info.get("upper_limit", "--"))
            ])

        if len(outlier_rows) == 1:
            outlier_rows.append([
                "No outliers detected",
                "-",
                "-",
                "-"
            ])

        outlier_table = Table(
            outlier_rows,
            colWidths=[
                45 * mm,
                30 * mm,
                40 * mm,
                40 * mm
            ]
        )

        outlier_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#6d00ff")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ])
        )

        story.append(outlier_table)

        # ==========================================
        # BUSINESS IMPACT
        # ==========================================

        story.append(
            Paragraph(
                "Business Impact",
                heading_style
            )
        )

        business = self.report.get(
            "business_impact",
            {}
        )

        for item in business.get(
            "business_impacts",
            []
        ):

            story.append(
                Paragraph(
                    f"<b>{item.get('issue', 'Issue')}</b>",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Severity:</b> "
                    f"{item.get('severity', 'Unknown')}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Impact:</b> "
                    f"{item.get('impact', '')}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Recommendation:</b> "
                    f"{item.get('recommendation', '')}",
                    normal_style
                )
            )

            story.append(Spacer(1, 5))

        # ==========================================
        # AI INSIGHTS
        # ==========================================

        story.append(
            Paragraph(
                "AI Recommendations",
                heading_style
            )
        )

        ai = self.report.get(
            "ai_insights",
            {}
        )

        for item in ai.get(
            "insights",
            []
        ):

            story.append(
                Paragraph(
                    f"<b>{item.get('type', 'AI Insight')}</b>",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    item.get(
                        "message",
                        ""
                    ),
                    normal_style
                )
            )

        # ==========================================
        # BUILD
        # ==========================================

        document.build(story)

        buffer.seek(0)

        return buffer
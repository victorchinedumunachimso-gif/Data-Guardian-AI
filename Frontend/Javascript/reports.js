// ========================================
// Data Guardian AI
// Executive Reports
// ========================================

console.log("✅ reports.js loaded");


document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log("🚀 Reports page starting...");


        // ========================================
        // GET SAVED ANALYSIS
        // ========================================

        const saved =
            localStorage.getItem(
                "analysisResult"
            );


        if (!saved) {

            console.warn(
                "⚠️ No analysis found in localStorage."
            );

            return;
        }


        try {

            const data =
                JSON.parse(saved);


            const report =
                data.executive_report;


            if (!report) {

                console.error(
                    "❌ executive_report not found."
                );

                return;
            }


            console.log(
                "📄 Executive report:",
                report
            );


            // ========================================
            // BASIC REPORT INFO
            // ========================================

            const reportTitle =
                document.getElementById(
                    "reportTitle"
                );

            if (reportTitle) {

                reportTitle.textContent =
                    report.title ||
                    "Data Guardian AI Executive Report";
            }


            const generatedAt =
                document.getElementById(
                    "generatedAt"
                );

            if (generatedAt) {

                generatedAt.textContent =
                    report.generated_at ||
                    "--";
            }


            // ========================================
            // QUALITY
            // ========================================

            const quality =
                report.overall_quality || {};


            const score =
                Number(
                    quality.score || 0
                );


            const qualityScore =
                document.getElementById(
                    "qualityScore"
                );

            if (qualityScore) {

                qualityScore.textContent =
                    `${score}%`;
            }


            const qualityGrade =
                document.getElementById(
                    "qualityGrade"
                );

            if (qualityGrade) {

                qualityGrade.textContent =
                    quality.grade ||
                    "Unknown";
            }


            const qualityProgress =
                document.getElementById(
                    "qualityProgress"
                );

            if (qualityProgress) {

                qualityProgress.style.width =
                    `${Math.max(
                        0,
                        Math.min(score, 100)
                    )}%`;
            }


            const qualitySummary =
                document.getElementById(
                    "qualitySummary"
                );

            if (qualitySummary) {

                qualitySummary.textContent =
                    report.executive_summary ||
                    "No executive summary available.";
            }


            // ========================================
            // PROFILE
            // ========================================

            const profile =
                report.dataset_profile || {};


            setText(
                "reportRows",
                profile.rows
            );

            setText(
                "reportColumns",
                profile.columns
            );

            setText(
                "profileRows",
                profile.rows
            );

            setText(
                "profileColumns",
                profile.columns
            );


            const memory =
                profile.memory_usage_mb;


            setText(
                "memoryUsage",
                memory !== undefined
                    ? `${memory} MB`
                    : "--"
            );


            // ========================================
            // VALIDATION
            // ========================================

            const validation =
                report.validation || {};


            const missingValues =
                validation.missing_values || {};


            const missingColumns =
                Object.keys(
                    missingValues
                ).length;


            const duplicateRows =
                validation.duplicate_rows || {};


            const duplicateCount =
                duplicateRows.count || 0;


            const emptyColumns =
                validation.empty_columns || [];


            setText(
                "missingColumns",
                missingColumns
            );


            setText(
                "duplicateRows",
                duplicateCount
            );


            setText(
                "emptyColumns",
                emptyColumns.length
            );


            // ========================================
            // OUTLIERS
            // ========================================

            const outliers =
                report.outliers || {};


            const totalOutliers =
                outliers.total_outliers || 0;


            setText(
                "reportOutliers",
                totalOutliers
            );


            renderOutliers(
                outliers
            );


            // ========================================
            // BUSINESS IMPACT
            // ========================================

            renderBusinessImpact(
                report.business_impact
            );


            // ========================================
            // AI RECOMMENDATIONS
            // ========================================

            renderRecommendations(
                report.ai_insights
            );


            // ========================================
            // EXECUTIVE SUMMARY
            // ========================================

            setText(
                "executiveSummary",
                report.executive_summary ||
                "No executive summary available."
            );


            // ========================================
            // DOWNLOAD
            // ========================================

            const downloadButton =
                document.getElementById(
                    "downloadReport"
                );


            if (downloadButton) {

                downloadButton.addEventListener(
                    "click",
                    function () {

                        downloadReport();

                    }
                );

            }


            console.log(
                "🎉 Reports page populated successfully!"
            );

        }


        catch (error) {

            console.error(
                "❌ Reports Error:",
                error
            );

        }

    }
);


// ========================================
// SET TEXT HELPER
// ========================================

function setText(
    id,
    value
) {

    const element =
        document.getElementById(id);


    if (!element) {
        return;
    }


    element.textContent =
        value ?? "--";
}


// ========================================
// OUTLIER TABLE
// ========================================

function renderOutliers(
    outliers
) {

    const container =
        document.getElementById(
            "outlierDetails"
        );


    if (!container) {
        return;
    }


    const columns =
        outliers?.columns || {};


    const entries =
        Object.entries(columns);


    if (entries.length === 0) {

        container.innerHTML = `

            <p class="empty-state">
                No outliers detected.
            </p>

        `;

        return;
    }


    container.innerHTML = `

        <table>

            <thead>

                <tr>

                    <th>Column</th>

                    <th>Outliers</th>

                    <th>Lower Limit</th>

                    <th>Upper Limit</th>

                </tr>

            </thead>

            <tbody>

                ${entries.map(
                    function ([column, info]) {

                        return `

                            <tr>

                                <td>
                                    ${column}
                                </td>

                                <td>
                                    ${info.count ?? 0}
                                </td>

                                <td>
                                    ${info.lower_limit ?? "--"}
                                </td>

                                <td>
                                    ${info.upper_limit ?? "--"}
                                </td>

                            </tr>

                        `;

                    }
                ).join("")}

            </tbody>

        </table>

    `;
}


// ========================================
// BUSINESS IMPACT
// ========================================

function renderBusinessImpact(
    business
) {

    const container =
        document.getElementById(
            "businessImpact"
        );


    if (!container) {
        return;
    }


    const impacts =
        business?.business_impacts || [];


    if (impacts.length === 0) {

        container.innerHTML = `

            <p class="empty-state">
                No major business impacts detected.
            </p>

        `;

        return;
    }


    container.innerHTML =
        impacts.map(
            function (item) {

                return `

                    <div class="impact-card">

                        <h3>
                            ${item.issue || "Issue"}
                        </h3>

                        <p>
                            <strong>
                                Severity:
                            </strong>

                            ${item.severity || "Unknown"}
                        </p>

                        <p>
                            <strong>
                                Impact:
                            </strong>

                            ${item.impact || ""}
                        </p>

                        <p>
                            <strong>
                                Recommendation:
                            </strong>

                            ${item.recommendation || ""}
                        </p>

                    </div>

                `;

            }
        ).join("");
}


// ========================================
// AI RECOMMENDATIONS
// ========================================

function renderRecommendations(
    ai
) {

    const container =
        document.getElementById(
            "aiRecommendations"
        );


    if (!container) {
        return;
    }


    const insights =
        ai?.insights || [];


    if (insights.length === 0) {

        container.innerHTML = `

            <p class="empty-state">
                No AI recommendations available.
            </p>

        `;

        return;
    }


    container.innerHTML =
        insights.map(
            function (item) {

                return `

                    <div class="recommendation-card">

                        <strong>
                            ${item.type || "AI Insight"}
                        </strong>

                        <p>
                            ${item.message || ""}
                        </p>

                    </div>

                `;

            }
        ).join("");
}


// ========================================
// PDF DOWNLOAD
// ========================================

// ========================================
// DOWNLOAD EXECUTIVE REPORT AS JSON
// ========================================

function downloadReport() {

    try {

        // Get saved analysis
        const saved =
            localStorage.getItem("analysisResult");

        if (!saved) {

            alert(
                "No analysis report is available. " +
                "Please analyze a dataset first."
            );

            return;
        }


        // Convert saved JSON string into object
        const data =
            JSON.parse(saved);


        console.log(
            "📦 Saved analysis data:",
            data
        );


        // ----------------------------------------
        // Find executive report
        // ----------------------------------------

        let report = null;


        // Normal structure from /analyze
        if (
            data &&
            typeof data === "object" &&
            data.executive_report &&
            typeof data.executive_report === "object"
        ) {

            report =
                data.executive_report;
        }


        // In case localStorage directly contains
        // the executive report
        else if (
            data &&
            typeof data === "object" &&
            data.overall_quality
        ) {

            report = data;
        }


        // ----------------------------------------
        // Safety check
        // ----------------------------------------

        if (!report) {

            console.error(
                "❌ Executive report not found:",
                data
            );

            alert(
                "Executive report data could not be found."
            );

            return;
        }


        // ----------------------------------------
        // Create downloadable JSON
        // ----------------------------------------

        const reportJSON =
            JSON.stringify(
                report,
                null,
                2
            );


        const blob =
            new Blob(
                [reportJSON],
                {
                    type:
                        "application/json;charset=utf-8"
                }
            );


        const url =
            URL.createObjectURL(blob);


        const link =
            document.createElement("a");


        link.href = url;


        // Filename
        link.download =
            "data_guardian_executive_report.json";


        document.body.appendChild(link);


        link.click();


        document.body.removeChild(link);


        // Release memory
        setTimeout(
            function () {

                URL.revokeObjectURL(url);

            },
            100
        );


        console.log(
            "✅ Executive report downloaded successfully!"
        );

    }

    catch (error) {

        console.error(
            "❌ Report download error:",
            error
        );

        alert(
            "Could not download the executive report: " +
            error.message
        );
    }
}
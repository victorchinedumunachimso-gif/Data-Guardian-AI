// ========================================
// Data Guardian AI
// Analysis Page
// ========================================

console.log("✅ analysis.js loaded");

document.addEventListener("DOMContentLoaded", function () {

    console.log("🚀 Analysis page starting...");

    // ========================================
    // GET SAVED ANALYSIS
    // ========================================

    const saved = localStorage.getItem("analysisResult");

    if (!saved) {

        console.warn("⚠️ No analysis data found.");

        showMessage(
            "No analysis available. Please upload and analyze a dataset first."
        );

        return;
    }


    // ========================================
    // PARSE DATA
    // ========================================

    let data;

    try {

        data = JSON.parse(saved);

        console.log("📊 Analysis data:", data);

    }

    catch (error) {

        console.error("❌ Could not parse analysis data:", error);

        showMessage("Unable to read the saved analysis.");

        return;
    }


    // ========================================
    // SUPPORT BOTH RESPONSE FORMATS
    // ========================================

    /*
        Format 1:

        {
            executive_report: {
                ...
            }
        }

        Format 2:

        {
            profile: {},
            validation: {},
            quality_score: {},
            ...
        }
    */

    const report =
        data.executive_report || data;


    console.log("📄 Using analysis report:", report);


    // ========================================
    // GET ANALYSIS SECTIONS
    // ========================================

    const profile =
        report.dataset_profile ||
        report.profile ||
        {};

    const validation =
        report.validation ||
        {};

    const quality =
        report.overall_quality ||
        report.quality_score ||
        {};

    const outliers =
        report.outliers ||
        {};

    const cleaning =
        report.cleaning ||
        {};

    const business =
        report.business_impact ||
        {};

    const ai =
        report.ai_insights ||
        {};

    const ml =
        report.ml_analytics ||
        {};


    // ========================================
    // QUALITY SCORE
    // ========================================

    const score =
        Number(
            quality.score ??
            quality.quality_score ??
            0
        );


    const scoreElement =
        document.getElementById("score");

    if (scoreElement) {

        scoreElement.textContent =
            `${score}%`;

    }


    // ========================================
    // QUALITY GRADE
    // ========================================

    const gradeElement =
        document.getElementById("qualityGrade");

    if (gradeElement) {

        gradeElement.textContent =
            quality.grade || "Unknown";

    }


    // ========================================
    // QUALITY DESCRIPTION
    // ========================================

    const descriptionElement =
        document.getElementById("qualityDescription");

    if (descriptionElement) {

        if (score >= 90) {

            descriptionElement.textContent =
                "Excellent dataset quality.";

        }

        else if (score >= 75) {

            descriptionElement.textContent =
                "Generally reliable with minor issues.";

        }

        else if (score >= 60) {

            descriptionElement.textContent =
                "Several issues require attention.";

        }

        else {

            descriptionElement.textContent =
                "Significant cleaning is required.";

        }

    }


    // ========================================
    // QUALITY RING
    // ========================================

    const qualityRing =
        document.getElementById("qualityRing");

    if (qualityRing) {

        const degrees =
            Math.max(0, Math.min(100, score)) * 3.6;

        let ringColor = "#ef4444";

        if (score >= 90) {

            ringColor = "#10b981";

        }

        else if (score >= 75) {

            ringColor = "#22c55e";

        }

        else if (score >= 60) {

            ringColor = "#f59e0b";

        }

        qualityRing.style.background =
            `conic-gradient(
                ${ringColor} ${degrees}deg,
                #e5e7eb ${degrees}deg
            )`;

    }


    // ========================================
    // DATASET ROWS
    // ========================================

    const rowsElement =
        document.getElementById("rows");

    if (rowsElement) {

        rowsElement.textContent =
            profile.rows ?? "--";

    }


    // ========================================
    // DATASET COLUMNS
    // ========================================

    const columnsElement =
        document.getElementById("columns");

    if (columnsElement) {

        columnsElement.textContent =
            profile.columns ?? "--";

    }


    // ========================================
    // MISSING VALUES
    // ========================================

    const missingValues =
        validation.missing_values || {};

    const missingCount =
        Object.values(missingValues)
            .reduce(function (total, value) {

                if (typeof value === "number") {

                    return total + value;

                }

                return total + 1;

            }, 0);


    const missingElement =
        document.getElementById("missing");

    if (missingElement) {

        missingElement.textContent =
            missingCount;

    }


    // ========================================
    // DUPLICATES
    // ========================================

    const duplicateRows =
        validation.duplicate_rows || {};

    const duplicateCount =
        Number(
            duplicateRows.count ??
            duplicateRows ??
            0
        );


    const duplicateElement =
        document.getElementById("duplicates");

    if (duplicateElement) {

        duplicateElement.textContent =
            duplicateCount;

    }


    // ========================================
    // EMPTY COLUMNS
    // ========================================

    const emptyColumns =
        validation.empty_columns || [];


    // ========================================
    // OUTLIERS
    // ========================================

    const outlierCount =
        Number(
            outliers.total_outliers ??
            0
        );


    // ========================================
    // TOTAL ISSUES
    // ========================================

    const issuesElement =
        document.getElementById("issues");

    if (issuesElement) {

        const totalIssues =
            missingCount +
            duplicateCount +
            emptyColumns.length +
            outlierCount;

        issuesElement.textContent =
            totalIssues;

    }


    // ========================================
    // VALIDATION PANEL
    // ========================================

    const validationElement =
        document.getElementById("validation");

    if (validationElement) {

        validationElement.innerHTML = `

            <div class="validation-item">

                <strong>
                    Missing Values
                </strong>

                <span>
                    ${missingCount}
                </span>

            </div>


            <div class="validation-item">

                <strong>
                    Duplicate Rows
                </strong>

                <span>
                    ${duplicateCount}
                </span>

            </div>


            <div class="validation-item">

                <strong>
                    Empty Columns
                </strong>

                <span>
                    ${emptyColumns.length}
                </span>

            </div>


            <div class="validation-item">

                <strong>
                    Outliers
                </strong>

                <span>
                    ${outlierCount}
                </span>

            </div>

        `;

    }


    // ========================================
    // AI INSIGHTS
    // ========================================

    const insightsElement =
        document.getElementById("insights");


    if (insightsElement) {

        let insights =
            ai.insights || [];


        if (!Array.isArray(insights)) {

            insights = [];

        }


        if (insights.length === 0) {

            insightsElement.innerHTML = `
                <p>No AI insights available.</p>
            `;

        }

        else {

            insightsElement.innerHTML =
                insights.map(function (item) {

                    return `

                        <div class="insight">

                            <h4>
                                ${item.type || "AI Insight"}
                            </h4>

                            <p>
                                ${item.message || item.insight || ""}
                            </p>

                        </div>

                    `;

                }).join("");

        }

    }


    // ========================================
    // CLEANING RESULTS
    // ========================================

    const cleaningElement =
        document.getElementById("cleaning");


    if (cleaningElement) {

        cleaningElement.innerHTML = `

            <div class="cleaning-item">

                <strong>
                    Duplicates Removed
                </strong>

                <span>
                    ${cleaning.duplicates_removed ?? 0}
                </span>

            </div>


            <div class="cleaning-item">

                <strong>
                    Empty Rows Removed
                </strong>

                <span>
                    ${cleaning.empty_rows_removed ?? 0}
                </span>

            </div>


            <div class="cleaning-item">

                <strong>
                    Rows After Cleaning
                </strong>

                <span>
                    ${cleaning.rows_after_cleaning ?? "--"}
                </span>

            </div>

        `;

    }


    // ========================================
    // ML ANALYTICS
    // ========================================

    console.log("🤖 ML Analytics:", ml);


    // ========================================
    // BUSINESS IMPACT
    // ========================================

    const businessElement =
        document.getElementById("businessImpact");


    if (businessElement) {

        const impacts =
            business.business_impacts || [];


        if (Array.isArray(impacts) && impacts.length > 0) {

            businessElement.innerHTML =
                impacts.map(function (item) {

                    return `

                        <div class="business-impact">

                            <h4>
                                ${item.issue || "Data Issue"}
                            </h4>

                            <p>
                                ${item.impact || ""}
                            </p>

                            <strong>
                                Recommendation:
                            </strong>

                            <p>
                                ${item.recommendation || ""}
                            </p>

                        </div>

                    `;

                }).join("");

        }

        else {

            businessElement.innerHTML =
                "<p>No business impact information available.</p>";

        }

    }


    // ========================================
    // SUCCESS
    // ========================================

    console.log(
        "🎉 Analysis page populated successfully!"
    );

});


// ========================================
// MESSAGE HELPER
// ========================================

function showMessage(message) {

    const containers = [

        document.getElementById("validation"),

        document.getElementById("insights")

    ];


    containers.forEach(function (element) {

        if (element) {

            element.innerHTML =
                `<p>${message}</p>`;

        }

    });

}
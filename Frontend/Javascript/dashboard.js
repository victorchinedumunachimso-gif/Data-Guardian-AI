// ========================================
// Data Guardian AI
// Dashboard
// ========================================

console.log("✅ dashboard.js loaded");


window.addEventListener("DOMContentLoaded", function () {

    console.log("🚀 Dashboard starting...");

    try {

        // ========================================
        // GET SAVED ANALYSIS
        // ========================================

        const saved =
            localStorage.getItem("analysisResult");

        console.log("💾 Saved analysis:", saved);


        if (!saved) {

            console.warn(
                "⚠️ No analysis found in localStorage."
            );

            showMessage(
                "validation",
                "No analysis found. Please analyze a dataset first."
            );

            return;
        }


        // ========================================
        // PARSE JSON
        // ========================================

        const data =
            JSON.parse(saved);

        console.log(
            "📦 Complete saved response:",
            data
        );


        // ========================================
        // GET ANALYSIS
        // ========================================

        /*
            Your backend now returns:

            {
                status: "Completed",
                analysis: {
                    profile: {},
                    validation: {},
                    outliers: {},
                    quality_score: {},
                    cleaning: {},
                    visualizations: {},
                    ml_analytics: {},
                    business_impact: {},
                    ai_insights: {}
                },
                ai: {}
            }
        */

        const analysis =
            data.analysis || {};


        // ========================================
        // QUALITY SCORE
        // ========================================

        const quality =
            analysis.quality_score || {};

        const score =
            Number(
                quality.quality_score ??
                quality.score ??
                0
            );


        const scoreElement =
            document.getElementById("score");

        if (scoreElement) {

            scoreElement.textContent =
                `${score}%`;
        }


        // ========================================
        // QUALITY RING
        // ========================================

        const qualityRing =
            document.getElementById(
                "qualityRing"
            );

        if (qualityRing) {

            const degrees =
                Math.max(
                    0,
                    Math.min(
                        score,
                        100
                    )
                ) * 3.6;


            let ringColor =
                "#ef4444";


            if (score >= 90) {

                ringColor =
                    "#10b981";

            } else if (score >= 75) {

                ringColor =
                    "#22c55e";

            } else if (score >= 60) {

                ringColor =
                    "#f59e0b";
            }


            qualityRing.style.background =
                `conic-gradient(
                    ${ringColor} ${degrees}deg,
                    #e5e7eb ${degrees}deg
                )`;
        }


        // ========================================
        // QUALITY GRADE
        // ========================================

        const qualityGrade =
            document.getElementById(
                "qualityGrade"
            );

        if (qualityGrade) {

            qualityGrade.textContent =
                quality.grade ||
                "Unknown";
        }


        // ========================================
        // QUALITY DESCRIPTION
        // ========================================

        const qualityDescription =
            document.getElementById(
                "qualityDescription"
            );

        if (qualityDescription) {

            if (score >= 90) {

                qualityDescription.textContent =
                    "Excellent dataset quality.";

            } else if (score >= 75) {

                qualityDescription.textContent =
                    "Generally reliable with minor issues.";

            } else if (score >= 60) {

                qualityDescription.textContent =
                    "Several issues require attention.";

            } else {

                qualityDescription.textContent =
                    "Significant cleaning is required.";
            }
        }


        // ========================================
        // DATASET PROFILE
        // ========================================

        const profile =
            analysis.profile || {};


        const rowsElement =
            document.getElementById("rows");

        if (rowsElement) {

            rowsElement.textContent =
                profile.rows ?? "--";
        }


        const columnsElement =
            document.getElementById("columns");

        if (columnsElement) {

            columnsElement.textContent =
                profile.columns ?? "--";
        }


        // ========================================
        // VALIDATION
        // ========================================

        const validation =
            analysis.validation || {};


        const missingValues =
            validation.missing_values || {};


        const missingColumns =
            Object.keys(
                missingValues
            ).length;


        const duplicateRows =
            validation.duplicate_rows || {};


        const duplicateCount =
            Number(
                duplicateRows.count ?? 0
            );


        const emptyColumns =
            validation.empty_columns || [];


        // ========================================
        // MISSING VALUES
        // ========================================

        const missingElement =
            document.getElementById("missing");

        if (missingElement) {

            missingElement.textContent =
                missingColumns;
        }


        // ========================================
        // DUPLICATES
        // ========================================

        const duplicateElement =
            document.getElementById("duplicates");

        if (duplicateElement) {

            duplicateElement.textContent =
                duplicateCount;
        }


        // ========================================
        // OUTLIERS
        // ========================================

        const outliers =
            analysis.outliers || {};


        const outlierCount =
            Number(
                outliers.total_outliers ?? 0
            );


        // ========================================
        // TOTAL DATASETS
        // ========================================

        const datasetsElement =
            document.getElementById(
                "datasets"
            );

        if (datasetsElement) {

            datasetsElement.textContent =
                "1";
        }


        // ========================================
        // REPORT COUNT
        // ========================================

        const reportsElement =
            document.getElementById(
                "reports"
            );

        if (reportsElement) {

            reportsElement.textContent =
                "1";
        }


        // ========================================
        // TOTAL ISSUES
        // ========================================

        const issuesElement =
            document.getElementById(
                "issues"
            );

        if (issuesElement) {

            const totalIssues =
                missingColumns +
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
            document.getElementById(
                "validation"
            );


        if (validationElement) {

            validationElement.innerHTML = `

                <p>
                    <strong>
                        Columns With Missing Values:
                    </strong>

                    ${missingColumns}
                </p>


                <p>
                    <strong>
                        Duplicate Rows:
                    </strong>

                    ${duplicateCount}
                </p>


                <p>
                    <strong>
                        Empty Columns:
                    </strong>

                    ${emptyColumns.length}
                </p>


                <p>
                    <strong>
                        Total Outliers:
                    </strong>

                    ${outlierCount}
                </p>

            `;
        }


        // ========================================
        // AI INSIGHTS
        // ========================================

        const insightsElement =
            document.getElementById(
                "insights"
            );


        if (insightsElement) {

            const ai =
                analysis.ai_insights || {};


            const insights =
                ai.insights || [];


            if (
                !Array.isArray(insights) ||
                insights.length === 0
            ) {

                insightsElement.innerHTML = `
                    <p>
                        No AI insights available.
                    </p>
                `;

            } else {

                insightsElement.innerHTML =
                    insights.map(
                        function (item) {

                            return `

                                <div class="insight">

                                    <strong>
                                        ${escapeHTML(
                                            item.type ||
                                            "Insight"
                                        )}
                                    </strong>

                                    <p>
                                        ${escapeHTML(
                                            item.message ||
                                            ""
                                        )}
                                    </p>

                                </div>

                            `;

                        }
                    ).join("");
            }
        }


        // ========================================
        // CLEANING
        // ========================================

        const cleaningElement =
            document.getElementById(
                "cleaning"
            );


        if (cleaningElement) {

            const cleaning =
                analysis.cleaning || {};


            cleaningElement.innerHTML = `

                <p>
                    <strong>
                        Duplicates Removed:
                    </strong>

                    ${cleaning.duplicates_removed ?? 0}
                </p>


                <p>
                    <strong>
                        Empty Rows Removed:
                    </strong>

                    ${cleaning.empty_rows_removed ?? 0}
                </p>


                <p>
                    <strong>
                        Values Filled:
                    </strong>

                    ${cleaning.values_filled ?? 0}
                </p>


                <p>
                    <strong>
                        Remaining Missing Values:
                    </strong>

                    ${cleaning.remaining_missing_values ?? 0}
                </p>


                <p>
                    <strong>
                        Rows After Cleaning:
                    </strong>

                    ${cleaning.rows_after_cleaning ?? 0}
                </p>

            `;
        }


        // ========================================
        // VISUALIZATION SUMMARY
        // ========================================

        const visualizations =
            analysis.visualizations || {};


        console.log(
            "📊 Visualization results:",
            visualizations
        );


        if (visualizations.charts) {

            console.log(
                "📈 Charts available:",
                visualizations.charts.length
            );

        }


        // ========================================
        // ML ANALYTICS
        // ========================================

        const mlAnalytics =
            analysis.ml_analytics || {};


        console.log(
            "🤖 ML Analytics:",
            mlAnalytics
        );


        // ========================================
        // BUSINESS IMPACT
        // ========================================

        const business =
            analysis.business_impact || {};


        console.log(
            "💼 Business Impact:",
            business
        );


        // ========================================
        // SUCCESS
        // ========================================

        console.log(
            "🎉 Dashboard populated successfully!"
        );

    }


    catch (error) {

        console.error(
            "❌ Dashboard Error:",
            error
        );


        showMessage(
            "validation",
            "Dashboard error: " +
            error.message
        );
    }

});


// ========================================
// HELPER: SHOW MESSAGE
// ========================================

function showMessage(
    elementId,
    message
) {

    const element =
        document.getElementById(
            elementId
        );

    if (element) {

        element.innerHTML = `
            <p>${escapeHTML(message)}</p>
        `;
    }
}


// ========================================
// HELPER: ESCAPE HTML
// ========================================

function escapeHTML(value) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        value ?? "";

    return div.innerHTML;
}


// ========================================
// SIDEBAR TOGGLE
// ========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const sidebar =
            document.querySelector(
                ".sidebar"
            );


        const mainContent =
            document.querySelector(
                ".main-content"
            );


        const toggleButton =
            document.getElementById(
                "sidebarToggle"
            );


        if (!sidebar) {

            console.warn(
                "⚠️ Sidebar not found"
            );

            return;
        }


        if (!mainContent) {

            console.warn(
                "⚠️ Main content not found"
            );

            return;
        }


        if (!toggleButton) {

            console.log(
                "ℹ️ No sidebar toggle button found."
            );

            return;
        }


        toggleButton.addEventListener(
            "click",
            function () {

                sidebar.classList.toggle(
                    "collapsed"
                );


                mainContent.classList.toggle(
                    "expanded"
                );


                console.log(
                    "✅ Sidebar toggled"
                );

            }
        );

    }
);
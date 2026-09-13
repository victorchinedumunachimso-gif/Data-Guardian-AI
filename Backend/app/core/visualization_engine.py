import pandas as pd
import numpy as np


class VisualizationEngine:

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe.copy()

        self.result = {
            "status": "Completed",
            "charts": []
        }

    # =====================================================
    # HELPERS
    # =====================================================

    def add_chart(
        self,
        chart_type,
        title,
        columns,
        reason,
        data=None
    ):

        chart = {
            "type": chart_type,
            "title": title,
            "columns": columns,
            "reason": reason
        }

        if data is not None:
            chart["data"] = data

        self.result["charts"].append(chart)

    # =====================================================
    # NUMERIC DISTRIBUTIONS
    # =====================================================

    def numeric_distributions(self):

        numeric_columns = (
            self.df
            .select_dtypes(include=np.number)
            .columns
            .tolist()
        )

        for column in numeric_columns:

            series = self.df[column].dropna()

            if len(series) == 0:
                continue

            # Limit data sent to frontend
            values = series.tolist()[:2000]

            self.add_chart(
                chart_type="histogram",
                title=f"Distribution of {column}",
                columns=[column],
                reason=(
                    "A histogram shows how values are distributed "
                    "and can reveal skewness and unusual values."
                ),
                data={
                    "x": values
                }
            )

    # =====================================================
    # CATEGORICAL FREQUENCIES
    # =====================================================

    def categorical_charts(self):

        categorical_columns = (
            self.df
            .select_dtypes(
                include=["object", "category", "bool"]
            )
            .columns
            .tolist()
        )

        for column in categorical_columns:

            # Avoid producing massive charts for high-cardinality
            # columns such as IDs, emails, phone numbers, etc.
            unique_count = self.df[column].nunique(
                dropna=True
            )

            if unique_count == 0:
                continue

            if unique_count > 15:
                continue

            counts = (
                self.df[column]
                .astype(str)
                .value_counts()
                .head(15)
            )

            self.add_chart(
                chart_type="bar",
                title=f"{column} Distribution",
                columns=[column],
                reason=(
                    "A bar chart compares the frequency of "
                    "different categories."
                ),
                data={
                    "x": counts.index.tolist(),
                    "y": counts.values.tolist()
                }
            )

    # =====================================================
    # CORRELATION
    # =====================================================

    def correlation_heatmap(self):

        numeric = (
            self.df
            .select_dtypes(include=np.number)
        )

        if numeric.shape[1] < 2:
            return

        correlation = numeric.corr()

        self.add_chart(
            chart_type="heatmap",
            title="Feature Correlation Heatmap",
            columns=numeric.columns.tolist(),
            reason=(
                "The correlation heatmap identifies strong "
                "positive and negative relationships between "
                "numeric variables."
            ),
            data={
                "columns":
                    correlation.columns.tolist(),

                "matrix":
                    correlation.fillna(0)
                    .round(4)
                    .values
                    .tolist()
            }
        )

    # =====================================================
    # SCATTER PLOTS
    # =====================================================

    def scatter_relationships(self):

        numeric_columns = (
            self.df
            .select_dtypes(include=np.number)
            .columns
            .tolist()
        )

        if len(numeric_columns) < 2:
            return

        # Use the first few columns to avoid generating
        # hundreds of combinations.
        selected = numeric_columns[:6]

        for i in range(len(selected)):

            for j in range(i + 1, len(selected)):

                x_column = selected[i]
                y_column = selected[j]

                pair = (
                    self.df[
                        [x_column, y_column]
                    ]
                    .dropna()
                    .head(2000)
                )

                if len(pair) < 2:
                    continue

                self.add_chart(
                    chart_type="scatter",
                    title=(
                        f"{y_column} vs {x_column}"
                    ),
                    columns=[
                        x_column,
                        y_column
                    ],
                    reason=(
                        "A scatter plot shows whether two "
                        "numeric variables have a visible "
                        "relationship or trend."
                    ),
                    data={
                        "x":
                            pair[x_column]
                            .tolist(),

                        "y":
                            pair[y_column]
                            .tolist()
                    }
                )

    # =====================================================
    # OUTLIER VIEW
    # =====================================================

    def outlier_charts(self):

        numeric_columns = (
            self.df
            .select_dtypes(include=np.number)
            .columns
            .tolist()
        )

        for column in numeric_columns:

            series = self.df[column].dropna()

            if len(series) < 5:
                continue

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - (1.5 * iqr)
            upper = q3 + (1.5 * iqr)

            outlier_mask = (
                (series < lower) |
                (series > upper)
            )

            outlier_count = int(
                outlier_mask.sum()
            )

            if outlier_count == 0:
                continue

            self.add_chart(
                chart_type="box",
                title=f"Outlier Analysis: {column}",
                columns=[column],
                reason=(
                    f"{outlier_count} potential outlier(s) "
                    "were detected using the IQR method."
                ),
                data={
                    "values":
                        series.tolist()[:2000],

                    "lower_limit":
                        float(lower),

                    "upper_limit":
                        float(upper)
                }
            )

    # =====================================================
    # BEFORE / AFTER CLEANING
    # =====================================================

    def cleaning_comparison(
        self,
        original_dataframe
    ):

        if original_dataframe is None:
            return

        original_missing = int(
            original_dataframe
            .isna()
            .sum()
            .sum()
        )

        cleaned_missing = int(
            self.df
            .isna()
            .sum()
            .sum()
        )

        self.add_chart(
            chart_type="comparison",
            title="Missing Values Before vs After Cleaning",
            columns=[],
            reason=(
                "This comparison shows how many missing "
                "values were removed or filled by the "
                "cleaning pipeline."
            ),
            data={
                "before":
                    original_missing,

                "after":
                    cleaned_missing
            }
        )

    # =====================================================
    # MAIN ANALYSIS
    # =====================================================

    def analyze(
        self,
        original_dataframe=None
    ):

        print(
            "📊 Starting automatic visualization analysis..."
        )

        self.numeric_distributions()

        print(
            "✅ Numeric distributions complete"
        )

        self.categorical_charts()

        print(
            "✅ Categorical charts complete"
        )

        self.correlation_heatmap()

        print(
            "✅ Correlation heatmap complete"
        )

        self.scatter_relationships()

        print(
            "✅ Scatter plots complete"
        )

        self.outlier_charts()

        print(
            "✅ Outlier charts complete"
        )

        self.cleaning_comparison(
            original_dataframe
        )

        print(
            "✅ Cleaning comparison complete"
        )

        self.result["total_charts"] = len(
            self.result["charts"]
        )

        print(
            f"🎉 Generated "
            f"{self.result['total_charts']} visualization(s)"
        )

        return self.result
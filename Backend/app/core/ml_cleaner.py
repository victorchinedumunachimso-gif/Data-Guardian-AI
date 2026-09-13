import pandas as pd
import numpy as np

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder

from sklearn.impute import SimpleImputer


class MLCleaner:

    def __init__(self, dataframe: pd.DataFrame):

        self.original_df = dataframe.copy()

        self.df = dataframe.copy()

        self.report = {
            "status": "Completed",
            "method": "Machine Learning",
            "columns_processed": 0,
            "values_filled": 0,
            "columns": {}
        }


    # =====================================================
    # PREPARE DATA
    # =====================================================

    def prepare_dataframe(self):

        df = self.df.copy()

        for column in df.columns:

            # Convert datetime columns to numeric timestamps
            if pd.api.types.is_datetime64_any_dtype(
                df[column]
            ):

                df[column] = (
                    df[column]
                    .astype("int64")
                    .replace(-9223372036854775808, np.nan)
                )

                df[column] = (
                    df[column] / 1_000_000_000
                )

        return df


    # =====================================================
    # IDENTIFY COLUMN TYPE
    # =====================================================

    def is_numeric_column(self, series):

        return pd.api.types.is_numeric_dtype(
            series
        )


    # =====================================================
    # BUILD PREPROCESSOR
    # =====================================================

    def build_preprocessor(
        self,
        X
    ):

        numeric_columns = X.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = X.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()


        numeric_pipeline = Pipeline([
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            )
        ])


        categorical_pipeline = Pipeline([
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                )
            )
        ])


        transformers = []


        if numeric_columns:

            transformers.append(
                (
                    "numeric",
                    numeric_pipeline,
                    numeric_columns
                )
            )


        if categorical_columns:

            transformers.append(
                (
                    "categorical",
                    categorical_pipeline,
                    categorical_columns
                )
            )


        return ColumnTransformer(
            transformers=transformers,
            remainder="drop"
        )


    # =====================================================
    # ML IMPUTE SINGLE COLUMN
    # =====================================================

    def impute_column(
        self,
        target_column
    ):

        column = self.df[target_column]

        missing_mask = column.isna()

        missing_count = int(
            missing_mask.sum()
        )


        if missing_count == 0:

            return


        # Need enough known values to train a model
        known_count = int(
            (~missing_mask).sum()
        )


        if known_count < 20:

            self.fallback_imputation(
                target_column
            )

            return


        feature_columns = [
            col
            for col in self.df.columns
            if col != target_column
        ]


        if not feature_columns:

            self.fallback_imputation(
                target_column
            )

            return


        X = self.df[
            feature_columns
        ].copy()


        y = self.df[
            target_column
        ].copy()


        # -------------------------------------------------
        # Split known/missing target rows
        # -------------------------------------------------

        train_mask = ~missing_mask

        X_train = X.loc[
            train_mask
        ]

        y_train = y.loc[
            train_mask
        ]

        X_missing = X.loc[
            missing_mask
        ]


        # -------------------------------------------------
        # Convert datetime features
        # -------------------------------------------------

        for frame in [
            X_train,
            X_missing
        ]:

            for col in frame.columns:

                if pd.api.types.is_datetime64_any_dtype(
                    frame[col]
                ):

                    frame[col] = (
                        frame[col]
                        .astype("int64")
                        .replace(
                            -9223372036854775808,
                            np.nan
                        )
                    )

                    frame[col] = (
                        frame[col]
                        / 1_000_000_000
                    )


        # -------------------------------------------------
        # Determine target type
        # -------------------------------------------------

        numeric_target = (
            self.is_numeric_column(column)
        )


        # -------------------------------------------------
        # Build preprocessing
        # -------------------------------------------------

        preprocessor = self.build_preprocessor(
            X_train
        )


        # =================================================
        # NUMERIC TARGET
        # =================================================

        if numeric_target:

            model = Pipeline([

                (
                    "preprocessor",
                    preprocessor
                ),

                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=100,
                        random_state=42,
                        n_jobs=-1
                    )
                )

            ])


        # =================================================
        # CATEGORICAL TARGET
        # =================================================

        else:

            # Remove rows where target itself is empty
            valid_target_mask = (
                y_train.notna()
            )

            X_train = X_train.loc[
                valid_target_mask
            ]

            y_train = y_train.loc[
                valid_target_mask
            ]


            # Classification needs at least two classes
            if y_train.nunique() < 2:

                self.fallback_imputation(
                    target_column
                )

                return


            model = Pipeline([

                (
                    "preprocessor",
                    preprocessor
                ),

                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=100,
                        random_state=42,
                        n_jobs=-1,
                        class_weight="balanced"
                    )
                )

            ])


        try:

            # -------------------------------------------------
            # Train ML model
            # -------------------------------------------------

            model.fit(
                X_train,
                y_train
            )


            # -------------------------------------------------
            # Predict missing values
            # -------------------------------------------------

            predictions = model.predict(
                X_missing
            )


            # -------------------------------------------------
            # Fill missing values
            # -------------------------------------------------

            self.df.loc[
                missing_mask,
                target_column
            ] = predictions


            self.report[
                "values_filled"
            ] += missing_count


            self.report[
                "columns_processed"
            ] += 1


            self.report[
                "columns"
            ][target_column] = {

                "missing_before": missing_count,

                "filled": missing_count,

                "method":
                    "Random Forest ML",

                "type":
                    "numeric"
                    if numeric_target
                    else "categorical"

            }


        except Exception as error:

            print(
                f"⚠️ ML failed for "
                f"{target_column}: {error}"
            )


            self.fallback_imputation(
                target_column
            )


    # =====================================================
    # FALLBACK
    # =====================================================

    def fallback_imputation(
        self,
        column
    ):

        missing_count = int(
            self.df[column]
            .isna()
            .sum()
        )


        if missing_count == 0:
            return


        try:

            if self.is_numeric_column(
                self.df[column]
            ):

                value = self.df[
                    column
                ].median()

                method = (
                    "Median fallback"
                )

            else:

                mode = self.df[
                    column
                ].mode()

                if len(mode) > 0:

                    value = mode.iloc[0]

                else:

                    value = "Unknown"

                method = (
                    "Mode fallback"
                )


            self.df[
                column
            ] = self.df[
                column
            ].fillna(value)


            self.report[
                "values_filled"
            ] += missing_count


            self.report[
                "columns_processed"
            ] += 1


            self.report[
                "columns"
            ][column] = {

                "missing_before":
                    missing_count,

                "filled":
                    missing_count,

                "method":
                    method,

                "type":
                    "numeric"
                    if self.is_numeric_column(
                        self.df[column]
                    )
                    else "categorical"

            }


        except Exception as error:

            print(
                f"❌ Fallback failed "
                f"for {column}: {error}"
            )


    # =====================================================
    # CLEAN DATASET
    # =====================================================

    def clean(self):

        print(
            "🤖 Starting ML-powered cleaning..."
        )


        # Work with a copy
        self.df = (
            self.prepare_dataframe()
        )


        columns = self.df.columns.tolist()


        for column in columns:

            if self.df[
                column
            ].isna().sum() > 0:

                print(
                    f"🔍 Learning how to fill: "
                    f"{column}"
                )

                self.impute_column(
                    column
                )


        self.report[
            "rows_after_cleaning"
        ] = len(self.df)


        self.report[
            "remaining_missing_values"
        ] = int(
            self.df.isna().sum().sum()
        )


        # -------------------------------------------------
        # Overall result
        # -------------------------------------------------

        if (
            self.report[
                "remaining_missing_values"
            ] == 0
        ):

            self.report[
                "message"
            ] = (
                "Machine learning successfully "
                "filled all missing values."
            )

        else:

            self.report[
                "message"
            ] = (
                "Machine learning cleaned the "
                "dataset, but some missing values "
                "remain."
            )


        print(
            "✅ ML cleaning completed"
        )


        return (
            self.df,
            self.report
        )
# ========================================
# Data Guardian AI
# Data Cleaner
# ========================================

import pandas as pd
import numpy as np


class DataCleaner:

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe.copy()

    def clean(self):

        report = {}

        # ========================================
        # Remove Duplicate Rows
        # ========================================

        duplicates_before = len(self.df)

        self.df = self.df.drop_duplicates()

        report["duplicates_removed"] = (
            duplicates_before - len(self.df)
        )

        # ========================================
        # Remove Completely Empty Rows
        # ========================================

        rows_before = len(self.df)

        self.df = self.df.dropna(how="all")

        report["empty_rows_removed"] = (
            rows_before - len(self.df)
        )

        # ========================================
        # Clean Columns
        # ========================================

        for column in self.df.columns:

            # ------------------------------------
            # Numeric Columns
            # ------------------------------------

            if pd.api.types.is_numeric_dtype(
                self.df[column]
            ):

                if self.df[column].isna().any():

                    median_value = self.df[column].median(
                        skipna=True
                    )

                    # Only fill if a valid median exists
                    if pd.notna(median_value):

                        self.df[column] = (
                            self.df[column]
                            .fillna(median_value)
                        )

            # ------------------------------------
            # Date / Datetime Columns
            # ------------------------------------

            elif pd.api.types.is_datetime64_any_dtype(
                self.df[column]
            ):

                if self.df[column].isna().any():

                    # Use the median date
                    valid_dates = self.df[column].dropna()

                    if not valid_dates.empty:

                        median_date = (
                            valid_dates
                            .sort_values()
                            .iloc[len(valid_dates) // 2]
                        )

                        self.df[column] = (
                            self.df[column]
                            .fillna(median_date)
                        )

            # ------------------------------------
            # Text / Categorical Columns
            # ------------------------------------

            else:

                # Keep missing values as actual NaN
                # while cleaning existing text values.

                self.df[column] = (
                    self.df[column]
                    .apply(
                        lambda value:
                        value.strip()
                        if isinstance(value, str)
                        else value
                    )
                )

                # Convert empty strings to NaN
                self.df[column] = (
                    self.df[column]
                    .replace(
                        r"^\s*$",
                        np.nan,
                        regex=True
                    )
                )

                # Fill missing text with the most
                # common value when possible.
                if self.df[column].isna().any():

                    mode = self.df[column].mode(
                        dropna=True
                    )

                    if not mode.empty:

                        self.df[column] = (
                            self.df[column]
                            .fillna(mode.iloc[0])
                        )

                    else:

                        self.df[column] = (
                            self.df[column]
                            .fillna("Unknown")
                        )

        # ========================================
        # Cleaning Report
        # ========================================

        report["rows_after_cleaning"] = len(self.df)

        report["columns_after_cleaning"] = (
            len(self.df.columns)
        )

        report["missing_values_after_cleaning"] = int(
            self.df.isna().sum().sum()
        )

        return self.df, report

    def summary(self):
        """
        Returns only the cleaning report.
        """

        _, report = self.clean()

        return report
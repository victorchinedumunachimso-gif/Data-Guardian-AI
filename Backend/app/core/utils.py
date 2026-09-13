"""
=========================================
Data Guardian AI
Core Utility Functions
=========================================
"""

import pandas as pd
import numpy as np


class DataUtils:
    """
    Utility functions used across the Data Guardian AI engine.
    """

    @staticmethod
    def memory_usage_mb(df: pd.DataFrame) -> float:
        """
        Calculate total memory usage of a dataframe in MB.
        """
        memory = df.memory_usage(deep=True).sum()
        return round(memory / (1024 ** 2), 2)

    @staticmethod
    def numeric_columns(df: pd.DataFrame):
        """
        Return numeric column names.
        """
        return list(df.select_dtypes(include=np.number).columns)

    @staticmethod
    def categorical_columns(df: pd.DataFrame):
        """
        Return categorical/text column names.
        """
        return list(df.select_dtypes(include=["object", "category"]).columns)

    @staticmethod
    def datetime_columns(df: pd.DataFrame):
        """
        Return datetime column names.
        """
        return list(df.select_dtypes(include=["datetime64"]).columns)

    @staticmethod
    def duplicate_rows(df: pd.DataFrame):
        """
        Count duplicate rows.
        """
        return int(df.duplicated().sum())

    @staticmethod
    def duplicate_percentage(df: pd.DataFrame):
        """
        Percentage of duplicate rows.
        """
        if len(df) == 0:
            return 0

        duplicates = df.duplicated().sum()

        return round((duplicates / len(df)) * 100, 2)

    @staticmethod
    def missing_values(df: pd.DataFrame):
        """
        Missing values for every column.
        """
        return df.isnull().sum().to_dict()

    @staticmethod
    def missing_percentage(df: pd.DataFrame):
        """
        Percentage of missing values.
        """
        percentages = {}

        for column in df.columns:

            percentages[column] = round(
                (df[column].isnull().sum() / len(df)) * 100,
                2
            )

        return percentages

    @staticmethod
    def empty_columns(df: pd.DataFrame):
        """
        Columns where every value is missing.
        """
        return [
            column
            for column in df.columns
            if df[column].isnull().all()
        ]

    @staticmethod
    def unique_values(df: pd.DataFrame):
        """
        Number of unique values per column.
        """
        return {
            column: int(df[column].nunique())
            for column in df.columns
        }

    @staticmethod
    def dataset_shape(df: pd.DataFrame):
        """
        Return rows and columns.
        """
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1])
        }

    @staticmethod
    def data_types(df: pd.DataFrame):
        """
        Data types of every column.
        """
        return {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        }

    @staticmethod
    def dataset_health_score(df: pd.DataFrame):
        """
        Calculate a simple health score.
        """

        score = 100

        score -= DataUtils.duplicate_percentage(df) * 0.5

        missing = sum(DataUtils.missing_percentage(df).values())

        score -= missing * 0.2

        score = max(score, 0)

        return round(score, 2)
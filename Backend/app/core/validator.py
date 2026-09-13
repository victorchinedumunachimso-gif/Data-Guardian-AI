import pandas as pd


class DataValidator:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def validate(self):

        report = {}

        # Missing values
        missing = self.df.isnull().sum()

        report["missing_values"] = {
            column: {
                "count": int(count),
                "percentage": round((count / len(self.df)) * 100, 2)
            }
            for column, count in missing.items()
            if count > 0
        }

        # Duplicate rows
        duplicate_rows = int(self.df.duplicated().sum())

        report["duplicate_rows"] = {
            "count": duplicate_rows,
            "percentage": round(
                (duplicate_rows / len(self.df)) * 100,
                2
            )
        }

        # Empty columns
        report["empty_columns"] = [
            column
            for column in self.df.columns
            if self.df[column].isnull().all()
        ]

        # Data types
        report["data_types"] = {
            column: str(dtype)
            for column, dtype in self.df.dtypes.items()
        }

        return report
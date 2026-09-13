import pandas as pd


class OutlierDetector:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def detect(self):

        report = {}

        total_outliers = 0

        for column in self.df.select_dtypes(include="number").columns:

            q1 = self.df[column].quantile(0.25)
            q3 = self.df[column].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - (1.5 * iqr)
            upper = q3 + (1.5 * iqr)

            mask = (self.df[column] < lower) | (
                self.df[column] > upper
            )

            count = int(mask.sum())

            total_outliers += count

            if count > 0:

                report[column] = {

                    "count": count,

                    "lower_limit": float(lower),

                    "upper_limit": float(upper)

                }

        return {

            "total_outliers": total_outliers,

            "columns": report

        }
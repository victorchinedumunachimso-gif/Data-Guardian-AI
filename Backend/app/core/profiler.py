import pandas as pd

class DataProfiler:
    def __init__(self, dataframe: pd.DataFrame):
        self.df=dataframe
    
    def profile(self):

        return{
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "column_names": list(self.df.columns),
            "data_types":{
                col: str(dtype)
                for col, dtype in self.df.dtypes.items()

            },
            "missing_values": self.df.isnull().sum().to_dict(),
            "duplicate_rows": int(self.df.duplicated().sum()),

            "memory_usage_mb":
            round(
                self.df.memory_usage(deep=True).sum() / 1024 / 1024, 2
            )

        }
        
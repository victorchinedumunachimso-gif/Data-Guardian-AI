import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest


class MLAnalytics:

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe.copy()

        self.result = {
            "status": "Completed",
            "correlations": {},
            "feature_importance": {},
            "anomalies": {},
            "pca": {},
            "clusters": {}
        }


    # =====================================================
    # NUMERIC DATA
    # =====================================================

    def numeric_data(self):

        numeric = self.df.select_dtypes(
            include=np.number
        ).copy()

        return numeric


    # =====================================================
    # CORRELATION ANALYSIS
    # =====================================================

    def correlation_analysis(self):

        numeric = self.numeric_data()

        if numeric.shape[1] < 2:

            self.result["correlations"] = {
                "status": "Not enough numeric columns"
            }

            return


        correlation_matrix = numeric.corr()

        correlations = {}

        for column in correlation_matrix.columns:

            correlations[column] = {}

            for other in correlation_matrix.columns:

                value = correlation_matrix.loc[
                    column,
                    other
                ]

                if pd.isna(value):
                    value = 0

                correlations[column][other] = round(
                    float(value),
                    4
                )


        self.result["correlations"] = correlations


    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================

    def feature_importance(self):

        numeric = self.numeric_data()

        if numeric.shape[1] < 2:

            self.result["feature_importance"] = {
                "status": "Not enough numeric columns"
            }

            return


        # Use the last numeric column as target
        target_column = numeric.columns[-1]

        features = [
            col
            for col in numeric.columns
            if col != target_column
        ]


        if not features:

            return


        X = numeric[features].copy()

        y = numeric[target_column].copy()


        # Fill any remaining missing values
        X = X.fillna(X.median())
        y = y.fillna(y.median())


        # Avoid model failure with constant target
        if y.nunique() < 2:

            self.result["feature_importance"] = {
                "status": "Target has insufficient variation"
            }

            return


        try:

            model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )

            model.fit(
                X,
                y
            )


            importance = {}

            for feature, value in zip(
                features,
                model.feature_importances_
            ):

                importance[feature] = round(
                    float(value),
                    4
                )


            # Highest importance first
            importance = dict(
                sorted(
                    importance.items(),
                    key=lambda item: item[1],
                    reverse=True
                )
            )


            self.result["feature_importance"] = {
                "target": target_column,
                "features": importance
            }


        except Exception as error:

            self.result["feature_importance"] = {
                "status": "Feature importance failed",
                "error": str(error)
            }


    # =====================================================
    # ANOMALY DETECTION
    # =====================================================

    def anomaly_detection(self):

        numeric = self.numeric_data()

        if numeric.shape[1] == 0:

            self.result["anomalies"] = {
                "status": "No numeric columns"
            }

            return


        numeric = numeric.fillna(
            numeric.median()
        )


        if len(numeric) < 10:

            self.result["anomalies"] = {
                "status": "Not enough rows"
            }

            return


        try:

            model = IsolationForest(
                contamination="auto",
                random_state=42,
                n_estimators=100
            )


            predictions = model.fit_predict(
                numeric
            )


            anomaly_mask = (
                predictions == -1
            )

            anomaly_count = int(
                anomaly_mask.sum()
            )


            anomaly_indices = (
                numeric.index[
                    anomaly_mask
                ]
                .tolist()
            )


            self.result["anomalies"] = {

                "algorithm":
                    "Isolation Forest",

                "total_anomalies":
                    anomaly_count,

                "percentage":
                    round(
                        (
                            anomaly_count /
                            len(numeric)
                        ) * 100,
                        2
                    ),

                "row_indices":
                    anomaly_indices[:100]

            }


        except Exception as error:

            self.result["anomalies"] = {

                "status":
                    "Anomaly detection failed",

                "error":
                    str(error)

            }


    # =====================================================
    # PCA
    # =====================================================

    def pca_analysis(self):

        numeric = self.numeric_data()

        if numeric.shape[1] < 2:

            self.result["pca"] = {
                "status": "At least 2 numeric columns required"
            }

            return


        numeric = numeric.fillna(
            numeric.median()
        )


        if len(numeric) < 2:

            return


        try:

            scaler = StandardScaler()

            scaled = scaler.fit_transform(
                numeric
            )


            pca = PCA(
                n_components=2
            )


            transformed = pca.fit_transform(
                scaled
            )


            points = []


            for index, point in zip(
                numeric.index,
                transformed
            ):

                points.append({

                    "row":
                        int(index)
                        if isinstance(
                            index,
                            (int, np.integer)
                        )
                        else str(index),

                    "PC1":
                        round(
                            float(point[0]),
                            5
                        ),

                    "PC2":
                        round(
                            float(point[1]),
                            5
                        )

                })


            self.result["pca"] = {

                "components":
                    2,

                "explained_variance": [

                    round(
                        float(
                            pca.explained_variance_ratio_[0]
                        ),
                        4
                    ),

                    round(
                        float(
                            pca.explained_variance_ratio_[1]
                        ),
                        4
                    )

                ],

                "points":
                    points[:1000]

            }


        except Exception as error:

            self.result["pca"] = {

                "status":
                    "PCA failed",

                "error":
                    str(error)

            }


    # =====================================================
    # CLUSTERING
    # =====================================================

    def clustering(self):

        numeric = self.numeric_data()

        if numeric.shape[1] < 2:

            self.result["clusters"] = {
                "status": "At least 2 numeric columns required"
            }

            return


        numeric = numeric.fillna(
            numeric.median()
        )


        if len(numeric) < 6:

            self.result["clusters"] = {
                "status": "Not enough rows"
            }

            return


        try:

            scaler = StandardScaler()

            scaled = scaler.fit_transform(
                numeric
            )


            # Keep number of clusters sensible
            k = min(
                3,
                len(numeric)
            )


            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10
            )


            labels = model.fit_predict(
                scaled
            )


            cluster_counts = {}

            for label in labels:

                label = int(label)

                cluster_counts[label] = (
                    cluster_counts.get(
                        label,
                        0
                    ) + 1
                )


            assignments = []


            for index, label in zip(
                numeric.index,
                labels
            ):

                assignments.append({

                    "row":
                        int(index)
                        if isinstance(
                            index,
                            (int, np.integer)
                        )
                        else str(index),

                    "cluster":
                        int(label)

                })


            self.result["clusters"] = {

                "algorithm":
                    "KMeans",

                "number_of_clusters":
                    k,

                "cluster_sizes":
                    cluster_counts,

                "assignments":
                    assignments[:1000]

            }


        except Exception as error:

            self.result["clusters"] = {

                "status":
                    "Clustering failed",

                "error":
                    str(error)

            }


    # =====================================================
    # RUN ALL ANALYSIS
    # =====================================================

    def analyze(self):

        print(
            "🤖 Starting ML analytics..."
        )


        self.correlation_analysis()

        print(
            "✅ Correlation analysis complete"
        )


        self.feature_importance()

        print(
            "✅ Feature importance complete"
        )


        self.anomaly_detection()

        print(
            "✅ Anomaly detection complete"
        )


        self.pca_analysis()

        print(
            "✅ PCA analysis complete"
        )


        self.clustering()

        print(
            "✅ Clustering complete"
        )


        print(
            "🎉 ML analytics completed"
        )


        return self.result
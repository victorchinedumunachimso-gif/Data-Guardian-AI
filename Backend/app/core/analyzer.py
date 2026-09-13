from typing import Dict, Any

import pandas as pd

from app.core.profiler import DataProfiler
from app.core.validator import DataValidator
from app.core.outlier_detector import OutlierDetector
from app.core.scorer import DataQualityScorer
from app.core.ml_cleaner import MLCleaner
from app.core.ml_analytics import MLAnalytics
from app.core.business_impact import BusinessImpactAnalyzer
from app.core.ai_insights import AIInsights
from app.core.visualization_engine import VisualizationEngine


class DataAnalyzer:

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe.copy()


    def analyze(self) -> Dict[str, Any]:

        print("🚀 Starting complete Data Guardian analysis...")


        # =====================================================
        # 1. PROFILE
        # =====================================================

        profiler = DataProfiler(
            self.df
        )

        profile = profiler.profile()

        print("✅ Profiling complete")


        # =====================================================
        # 2. VALIDATION
        # =====================================================

        validator = DataValidator(
            self.df
        )

        validation = validator.validate()

        print("✅ Validation complete")


        # =====================================================
        # 3. OUTLIER DETECTION
        # =====================================================

        detector = OutlierDetector(
            self.df
        )

        outliers = detector.detect()

        print("✅ Outlier detection complete")


        # =====================================================
        # 4. QUALITY SCORE
        # =====================================================

        scorer = DataQualityScorer(
            validation_result=validation,
            outlier_result=outliers
        )

        score = scorer.calculate_score()

        print("✅ Quality score complete")

        print("📊 Quality score:", score)


        # =====================================================
        # 5. MACHINE LEARNING CLEANING
        # =====================================================

        ml_cleaner = MLCleaner(
            self.df
        )

        cleaned_df, cleaning_report = (
            ml_cleaner.clean()
        )

        print("✅ ML cleaning complete")

        visualization_engine = VisualizationEngine(
        cleaned_df
)

        visualization_results = (visualization_engine.analyze(
        original_dataframe=self.df
)
        )


        # =====================================================
        # 6. MACHINE LEARNING ANALYTICS
        # =====================================================

        ml_analytics_engine = MLAnalytics(
            cleaned_df
        )

        ml_results = (
            ml_analytics_engine.analyze()
        )

        print("✅ ML analytics complete")


        # =====================================================
        # 7. BUSINESS IMPACT
        # =====================================================

        business = BusinessImpactAnalyzer(
            validation_result=validation,
            outlier_result=outliers
        )

        business_report = (
            business.analyse()
        )

        print("✅ Business impact complete")


        # =====================================================
        # 8. AI INSIGHTS
        # =====================================================

        ai = AIInsights(
            validation_report=validation,
            score_report=score,
            business_report=business_report,
            outlier_report=outliers
        )

        ai_report = ai.generate()

        print("✅ AI insights complete")


        # =====================================================
        # 9. BUILD COMPLETE ANALYSIS RESULT
        # =====================================================

        analysis_result = {

            "status": "success",

            "profile":
                profile,

            "validation":
                validation,

            "outliers":
                outliers,

            "quality_score":
                score,

            "cleaning":
                cleaning_report,

            "ml_analytics":
                ml_results,

            "business_impact":
                business_report,

            "ai_insights":
                ai_report,
            "visualizations": 
                visualization_results
        }


        # =====================================================
        # SAFETY CHECK
        # =====================================================

        if "quality_score" not in analysis_result:

            raise RuntimeError(
                "quality_score was not created "
                "during analysis."
            )


        print(
            "🎉 Complete analysis finished successfully!"
        )

        return analysis_result
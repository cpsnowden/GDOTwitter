import logging

from AnalysisEngine.CeleryApp import app
from AnalysisEngine.AnalysisRouter import AnalysisRouter
from api.Objects.MetaData import AnalyticsMeta
from datetime import datetime
logger = logging.getLogger(__name__)

@app.task
def get_analytics(analytics_id):

    logger.info("Attempting to get analytics: "+ analytics_id)

    analytics_meta = AnalyticsMeta.objects.get(id=analytics_id)
    logger.info(analytics_meta.classification + " " + analytics_meta.type)

    result = AnalysisRouter.process(analytics_meta)

    if result:
        logger.info("Analytics task %s successful", analytics_meta.id)
        analytics_meta.end_time = datetime.now()
        analytics_meta.status = "FINISHED"
        analytics_meta.save()
from celery import Celery

app = Celery("analytics", broker='amqp://guest@localhost//', include=["AnalysisEngine.AnalysisTasks"])
# app.conf.update(
#     CELERY_RESULT_BACKEND = 'mongodb://localhost:27017/',
#     CELERY_MONGODB_BACKEND_SETTINGS = {
#     'database': 'mydb',
#         'user': "twitterApplication",
#         'password': "gdotwitter",
#         'taskmeta_collection': 'my_taskmeta_collection'
#     }
# )


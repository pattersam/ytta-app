from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "worker",
    broker="sqs://",
    task_default_queue="ytta-celery",
    broker_transport_options={
        "predefined_queues": {
            "ytta-celery": {
                "url": settings.SQS_URL,
            },
        },
    },
)

celery_app.conf.task_routes = {
    "app.worker.test_celery": "ytta-celery",
    "app.worker.analyse_video": "ytta-celery",
}

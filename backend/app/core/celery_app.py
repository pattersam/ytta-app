from celery import Celery

celery_app = Celery(
    "worker",
    broker="sqs://",
    task_default_queue="ytta-celery",
    broker_transport_options={
        "predefined_queues": {
            "ytta-celery": {
                "url": "https://sqs.eu-central-1.amazonaws.com/407298002065/ytta-celery",
            },
        },
    },
)

celery_app.conf.task_routes = {
    "app.worker.test_celery": "ytta-celery",
    "app.worker.analyse_video": "ytta-celery",
}

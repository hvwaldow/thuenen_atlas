from django.apps import AppConfig
from django.conf import settings
from django.conf.urls import include, url


import logging

logger = logging.getLogger(__name__)


BASE_FILE = "pushed_resource"
XML_FILE = "metadata"
THUMBNAIL_FILE = "thumbnail"
STYLE_FILE = "style"
DATA_FILE = "data"


def run_setup_hooks(*args, **kwargs):
    from geonode.urls import urlpatterns
    from geonode.api.urls import router
    from .api import views

    settings.CELERY_BEAT_SCHEDULE["push-to-remote"] = {
        "task": "sync.tasks.scheduler",
        "schedule": getattr(settings, "PUSH_TO_REMOTE_SCHEDULER_FREQUENCY_MINUTES", 0.5) * 60,
    }

    urlpatterns += [url(r"^sync/receive", views.ReceivePushedDataViewSet.as_view())]


class SyncConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sync"
    type = "GEONODE_APP"

    def ready(self):
        super().ready()
        run_setup_hooks()

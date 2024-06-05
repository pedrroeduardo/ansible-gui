from django.urls import re_path
from . import consumers

urlpatterns = [
    re_path(r'ws/run_job/(?P<id>\d+)/$', consumers.RunJobConsumer.as_asgi()),
]

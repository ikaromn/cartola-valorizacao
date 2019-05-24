from django.conf.urls import url

from cartola_mn.apps.player.views import Players

urlpatterns = [
    url(r'^$', Players.as_view()),
]

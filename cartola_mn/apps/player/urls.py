from django.conf.urls import url

from cartola_mn.apps.player.views import Players, PartialScore, TeamPartialScore

urlpatterns = [
    url(r'^$', Players.as_view()),
    url(r'^partials/$', PartialScore.as_view()),
    url(r'^partials/teams/$', TeamPartialScore.as_view()),
]

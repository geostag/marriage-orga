from django.conf.urls import include, url
import backend.views

urlpatterns = [
    url(r'^event/(?P<id>.+)/$',                  backend.views.event,name="backend.event"),
    url(r'^participant/add/(?P<id>.+)/$',        backend.views.participant_add,name="backend.participant.add"),
    url(r'^participant/remove/(?P<id>.+)/$',     backend.views.participant_remove,name="backend.participant.remove"),
    url(r'^participant/set/$',        backend.views.participant_set,name="backend.participant.set"),
]

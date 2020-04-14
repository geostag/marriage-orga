from django.conf.urls import include, url
import event.views

urlpatterns = [
    url(r'^leave/$',                  event.views.leave,name="event.leave"),
    url(r'^enter/$',                  event.views.enter,name="event.enter"),
    url(r'^enter/(?P<shortcut>.+)/$', event.views.enter,name="event.enter"),
    url(r'^participate/$',            event.views.participate,name="event.participate"),
    url(r'^participant/set/$',        event.views.participant_set,name="event.participant.set"),
    url(r'^participant/add/$',        event.views.participant_add,name="event.participant.add"),
    url(r'^participant/remove/(?P<gid>\d+)/$',     event.views.participant_remove,name="event.participant.remove"),
    url(r'^ci/set/$',                 event.views.ci_set,name="event.ci.set"),
]

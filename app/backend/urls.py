from django.conf.urls import include, url
import backend.views

urlpatterns = [
    url(r'^enter/$',                  backend.views.base,name="backend.base"),
    url(r'^event/(?P<id>.+)/$',                  backend.views.event,name="backend.event"),
    url(r'^participant/add/(?P<id>.+)/$',        backend.views.participant_add,name="backend.participant.add"),
    url(r'^participant/remove/(?P<id>.+)/$',     backend.views.participant_remove,name="backend.participant.remove"),
    url(r'^participant/set/$',                   backend.views.participant_set,name="backend.participant.set"),
    url(r'^coli/add/(?P<col_id>.+)/$',           backend.views.coli_add,name="backend.coli.add"),
    url(r'^coli/edit/(?P<coli_id>.+)/$',         backend.views.coli_edit,name="backend.coli.edit"),
    url(r'^coli/delete/(?P<coli_id>.+)/$',       backend.views.coli_delete,name="backend.coli.delete"),
    url(r'^information/add/(?P<event_id>.+)/$',  backend.views.document_add,name="backend.document.add"),
    url(r'^information/edit/(?P<document_id>.+)/$', backend.views.document_edit,name="backend.document.edit"),
]

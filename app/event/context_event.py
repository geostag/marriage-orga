"""
Export current customer to templates

"""
from django.core.exceptions import ImproperlyConfigured
from backend.models import Event, Participant

__version__ = '1.0'


def event_export(request):
    e = Event.getfromsession(request)
    p = Participant.getfromsession(request)
    return { "event": e, "participant": p }



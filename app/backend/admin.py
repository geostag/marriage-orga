from django.contrib import admin
from backend.models import Event, Participant, Contribution, Document

# Register your models here.
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Contribution)
admin.site.register(Document)

from django.contrib import admin
from backend.models import Event, Participant, Contribution, Document, Ci, Checkoutlist, Coli

# Register your models here.
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Contribution)
admin.site.register(Ci)
admin.site.register(Document)
admin.site.register(Checkoutlist)
admin.site.register(Coli)

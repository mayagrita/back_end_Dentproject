from .models import Patient, Diagnosis, Note
from django.contrib import admin

admin.site.register(Patient)
admin.site.register(Diagnosis)
admin.site.register(Note)
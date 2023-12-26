from django.contrib import admin
from .models import Incident, Handler

# Register your models here.

admin.site.register(Incident)
admin.site.register(Handler)
from django.contrib import admin
from .models import Profile, EventUser, EventLog

admin.site.register(Profile)
admin.site.register(EventUser)
admin.site.register(EventLog)

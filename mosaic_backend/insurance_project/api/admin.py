from django.contrib import admin
from .models import Client, Policy

admin.site.register(Client)
admin.site.register(Policy)
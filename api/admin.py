from django.contrib import admin
from .models import SmartBin

@admin.register(SmartBin)
class SmartBinAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active')
    search_fields = ('name', 'location')
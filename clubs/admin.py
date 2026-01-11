from django.contrib import admin
from .models import Club, EcoDrive

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    search_fields = ("name",)
    filter_horizontal = ("members",)
    
admin.site.register(EcoDrive)

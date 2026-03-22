from django.contrib import admin
from .models import User, UserFaceEmbedding

admin.site.register(User)


@admin.register(UserFaceEmbedding)
class UserFaceEmbeddingAdmin(admin.ModelAdmin):
	list_display = ("user", "model_name", "updated_at")
	search_fields = ("user__username", "model_name")

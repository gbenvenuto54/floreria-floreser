from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "model", "object_id", "user", "ip")
    list_filter = ("action", "model", "created_at")
    search_fields = ("model", "object_id", "detail", "user__username", "ip")
    date_hierarchy = "created_at"

from django.contrib import admin
from .models import ScanResult
# Register your models here.

@admin.register(ScanResult)
class ScanResult(admin.ModelAdmin):
    list_display = ('user', 'url', 'report')

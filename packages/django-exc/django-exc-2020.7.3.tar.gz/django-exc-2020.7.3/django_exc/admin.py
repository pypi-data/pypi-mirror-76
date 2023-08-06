from django.contrib import admin

from .models import Exc


class ExcAdmin(admin.ModelAdmin):
    list_display = ('exc_type', 'exc_value', 'exc_traceback', 'created_at',)
    list_filter = ('exc_type',)

admin.site.register(Traceback, ExcAdmin)

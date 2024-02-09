from django.contrib import admin

from .models import DailyReport


class DailyReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'send_time']
    filter_horizontal = ['recipients']


admin.site.register(DailyReport, DailyReportAdmin)

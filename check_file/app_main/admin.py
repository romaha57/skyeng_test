from django.contrib import admin

from .models import UploadFile
from import_export.admin import ImportExportModelAdmin


class UploadFileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'file', 'status', 'is_check', 'is_right')
    list_filter = ('user', 'status')
    search_fields = ('user',)
    readonly_fields = ('is_right', 'is_check')
    search_help_text = 'поиск по пользователю'


admin.site.register(UploadFile, UploadFileAdmin)

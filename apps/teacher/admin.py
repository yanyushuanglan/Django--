from django.contrib import admin
from apps.student.models import TeacherTable
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class TeacherTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['tea_id', 'tea_name','sex','position', 'tea_title']
    search_fields = ('tea_id', 'tea_name', 'tea_title')

admin.site.register(TeacherTable,TeacherTableAdmin)
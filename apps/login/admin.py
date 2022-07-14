from django.contrib import admin
from .models import *
# Register your models here.
from import_export.admin import ImportExportModelAdmin
class UPC_UserAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['u_name','u_type']

admin.site.register(UPC_User,UPC_UserAdmin)


admin.site.site_header = '教务管理系统后台'  # 设置header
admin.site.site_title = '教务管理系统后台'   # 设置title
admin.site.index_title = '教务管理系统后台'
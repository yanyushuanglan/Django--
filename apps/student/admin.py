from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *

# Register your models here.


class CollegeTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['college_id', 'college_name']
    search_fields = ('college_id', 'college_name')

class StudentTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['stu_id', 'stu_name','sex', 'stu_class','college']
    # list_editable = ['stu_id', 'stu_name', 'stu_class']
    search_fields = ('stu_id', 'stu_name')

class CourseTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['course_id', 'course_name', 'CourseNature']
    search_fields = ('course_id', 'course_name')

class ScoreTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['student','open',  'score','GradePoint']
    list_filter = ['student','open' ]
    search_fields = ('student', 'open')

class OpenTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['year', 'semester','course', 'teacher']
    list_filter = ['course', 'teacher' ]
    search_fields = ('year', 'semester','course', 'teacher')

class NoticeTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['title', 'time']
    search_fields = ('title','time')

class LeaveTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['uid', 'uname', 'agreeTeacher', 'isAgree']
    search_fields = ('uid','uname','type')

class PunishmentTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['uid', 'uname', 'type', 'examine', 'iscancel', 'createtime']
    search_fields = ('uid', 'uname', 'agreeTeacher')
class ClassTableAdmin(ImportExportModelAdmin):
    list_per_page = 10
    list_display = ['className', 'nianJ', 'college']
    list_filter = ['college']
    search_fields = ('className', 'nianJ', 'college')

class JurisdictionTableAdmin(ImportExportModelAdmin):
    list_display = ['IsAddScore', 'IsModify', 'IsCancel','IsLeave','IsChoice']

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False


admin.site.register(JurisdictionTable,JurisdictionTableAdmin)#注册权限表

admin.site.register(ClassTable,ClassTableAdmin)#注册班级表

admin.site.register(CollegeTable,CollegeTableAdmin)#注册院系表

admin.site.register(StudentTable,StudentTableAdmin)#注册学生信息表

admin.site.register(ScoreTable,ScoreTableAdmin)#注册选课成绩表

admin.site.register(OpenTable,OpenTableAdmin)#注册开课表

admin.site.register(CourseTable,CourseTableAdmin)#注册课程表

admin.site.register(NoticeTable,NoticeTableAdmin)#注册通知公告表

admin.site.register(LeaveTable,LeaveTableAdmin)#注册请假表

admin.site.register(PunishmentTable,PunishmentTableAdmin)#注册违纪处分表
from .views import *
from django.urls import path

urlpatterns = [
    path('test/',test,name = 'test'),
    # path('stu_base/',stu_base,name='stu_base'),
    path('stu_index/',stu_index,name = 'stu_index'),
    path('stu_mssg/',stu_mssg,name = 'stu_mssg'),
    path('stu_score/',stu_score,name = 'stu_score'),
    path('stu_choiceCourse/',stu_choiceCourse,name = 'stu_choiceCourse'),
    path('stu_myCourse/',stu_myCourse,name = 'stu_myCourse'),
    path('stu_leave/',stu_leave,name = 'stu_leave'),
    path('stu_punishment/',stu_punishment,name = 'stu_punishment'),
    path('stu_notice/',stu_notice,name = 'stu_notice'),
    path('stu_idcard/',stu_idcard,name = 'stu_idcard'),
    path('stu_queryScore/',stu_queryScore,name = 'stu_queryScore'),
    path('stu_OnlineCourse/<int:id>',stu_OnlineCourse,name = 'stu_OnlineCourse'),
    path('Leave/',Leave,name = 'Leave'),

]

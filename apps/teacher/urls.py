
from django.urls import path
from .views import *

urlpatterns = [
    path('index/',tea_index,name='index'),
    path('message/',tea_mssg,name="message"),
    # path('returnmssg/',tea_returnmssg,name="returnmssg"),
    path('selectmessage/',tea_select,name="selectmessage"),
    path('writescore/',tea_writeScore,name="writescore"),
    path('addscore/<int:id>',tea_addScore,name="addscore"),
    path('punishment/', tea_studentcf, name="punishment"),
    path('cxpunishment/<int:id>', tea_cxPunishment, name="cxpunishment"),
    path('stuleave/', tea_studentLeave, name="stuleave"),
    path('examineLeave/<int:id>', tea_examineLeave, name="examineLeave"),
    path('myclass/', tea_myClass, name="myclass"),
    path('notice/', tea_notice,name="notice"),
    path('file_up/',batch_pay_deal,name="file_up"),
    path('excel_export/<int:id>',excel_export,name="excel_export")
]
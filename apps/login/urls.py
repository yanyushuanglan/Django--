from django.urls import path
from .views import *

urlpatterns = [
    path('login/',login,name='login'),
    path('outlogin/',outlogin,name='outlogin')
    # path('stu_base/',stu_base,name='stu_base'),
]
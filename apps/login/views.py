from functools import wraps

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from apps.student.models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        content = UPC_User.objects.filter(u_uid=name, u_password=password)
        if len(content):
            isTeacher = UPC_User.objects.values('u_type').filter(u_uid=name, u_password=password)
            if isTeacher[0]['u_type']:
                request.session['user'] = {
                    'username': name,
                    'password': password,
                    'islogin':True
                }
                request.session.set_expiry(0)
                return render(request, 'base/tea_base.html', {'content': content})
            else:
                request.session['user'] = {
                    'username': name,
                    'password': password,
                    'islogin': True
                }
                request.session.set_expiry(0)
                return render(request, 'base/stu_base.html', {'content': content})
        else:
            return render(request, 'login.html', {'conent': '密码或用户名错误'})
    else:
        return render(request, 'login.html')

def outlogin(request):
    request.session.pop('user')
    return redirect('/login/')

class UserMethod:
    def __init__(self, request):
        self.request = request
        self.uinfo = self.getUserInfo()  # 运行判断
    # 判断是否登录
    def getUserInfo(self):
        if 'user' in self.request.session:
            return self.request.session['user']
        else:
            return {'islogin': False}

def login_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        thisuser = UserMethod(request)
        userinfo = thisuser.getUserInfo()
        if userinfo['islogin'] is not True: #如果没有登录则返回登录页面
            return HttpResponseRedirect('/login/')
        return f(request, *args, **kwargs)
    return decorated_function

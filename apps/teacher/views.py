import os

import xlrd
import xlwt
from django.core import serializers
from django.http import JsonResponse, response
from django.shortcuts import render,HttpResponse
from xlwt import Workbook

from apps.student.models import *
from django.views.decorators.csrf import csrf_exempt
from apps.login.views import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import math
from io import BytesIO
# Create your views here.

def session(request):
    us = request.session['user']
    teaid = us['username']
    inifo = TeacherTable.objects.filter(tea_id=teaid)
    return inifo

@login_required
def tea_index(request):  # 首页

    return render(request, 'tea_index.html', {'inifo': session(request)})

@login_required
def tea_mssg(request):  # 个人信息

    return render(request, 'tea_mymssg.html', {'inifo': session(request)})


def pager(request,info):
    cl = ClassTable.objects.all()
    # 获取当前页码数
    num = request.GET.get('num', 1)
    n = int(num)

    # # 查询所有数据
    # stu = StudentTable.objects.all()

    # 创建分页器对象
    pager = Paginator(info, 10)

    # 获取当前页的数据
    try:
        perpage_data = pager.page(n)
    except PageNotAnInteger:
        # 返回第一页的数据
        perpage_data = pager.page(1)
    except EmptyPage:
        # 返回最后一页的数据
        perpage_data = pager.page(pager.num_pages)

    # 每页开始页码
    begin = (n - int(math.ceil(10.0 / 2)))
    if begin < 1:
        begin = 1

    # 每页结束页码
    end = begin + 9
    if end > pager.num_pages:
        end = pager.num_pages

    if end <= 10:
        begin = 1
    else:
        begin = end - 9

    pagelist = range(begin, end + 1)
    return {'inifo': session(request),'pager': pager, 'perpage_data': perpage_data, 'pagelist': pagelist, 'currentPage': n,'class':cl}


@login_required
@csrf_exempt
def tea_select(request):  # 查询学生信息
    if request.method == 'POST':
        name = request.POST.get('cname')
        if name is not None:
            stuinfo = StudentTable.objects.filter(stu_class__className=name)
            return render(request, 'tea_xsmssgck.html',pager(request,stuinfo))
        else:
            return render(request, 'tea_xsmssgck.html', {'inifo': session(request), 'mssg': '请输入完整班级名称'})
    else:
        stuinfo = StudentTable.objects.all()
        return render(request, 'tea_xsmssgck.html',pager(request,stuinfo))


@login_required
@csrf_exempt
def tea_writeScore(request): #学生成绩管理
    us = request.session['user']
    teaid = us['username']
    if request.method == 'POST':
        courseName = request.POST.get('cname')
        writeinfo = OpenTable.objects.values('course__credit',
                                          'course__CourseNature',
                                          'course__course_id',
                                          'teacher__tea_name',
                                          'semester',
                                          'year',
                                          'scoretable__score',
                                          'scoretable__GradePoint',
                                          'scoretable__student__stu_id',
                                          'scoretable__student__stu_name',
                                          'scoretable__student__stu_class',
                                          'course__course_name',
                                          'scoretable__id'
                                          ).filter(course__course_name=courseName)

        courseinfo = CourseTable.objects.filter(opentable__teacher__tea_id=teaid)
        return render(request, 'tea_xsScore.html', {'inifo': session(request), "writeinfo": writeinfo,'courseinfo': courseinfo})
    else:
        courseinfo = CourseTable.objects.filter(opentable__teacher__tea_id=teaid)
        return render(request, 'tea_xsScore.html', {'inifo': session(request), 'courseinfo': courseinfo})


def batch_pay_deal(request):

    if request.method == "POST":
        # 获取普通input标签值，即文件名
        filename = request.POST.get('fileName')
        # 获取file类型的input标签值，即文件内容
        file = request.FILES.get('fileContent')

        data = xlrd.open_workbook(
            filename=None, file_contents=file.read())  # 读取表格
        table = data.sheets()[0]  # 第一张表单
        row = table.nrows
        for i in range(1, row):  # 跳过第0行
            col = table.row_values(i)
            name = col[0]
            stuid = str(int(col[1]))
            courseName = col[2]
            score = float(col[3])
            gd = score / 10 - 5
            print(stuid,name,courseName,score,gd)

            ScoreTable.objects.filter(student__stu_name=name,
                                      student__stu_id=stuid,
                                      open__course__course_name=courseName
                                      ).update(score=round(score,1),GradePoint=round(gd,1))

            writeinfo = ScoreTable.objects.filter(open__course__course_name=courseName)
            scinfo = serializers.serialize("json", writeinfo)  # 序列化
            print(scinfo)
        return JsonResponse({'result': 'ok','scinfo':scinfo})
    else:
        return JsonResponse({'result': 'no'})








@login_required
@csrf_exempt
def tea_addScore(request,id):#录入成绩
    qxobj = JurisdictionTable.objects.values('IsAddScore')
    qx = qxobj[0]['IsAddScore']
    if qx and request.method == 'POST':
        try:
            sc = float(request.POST.get('score'))
        except:
            return HttpResponse('请输入数字')
        else:
            if 0 <= sc <= 100:
                us = request.session['user']
                teaid = us['username']
                cn = ScoreTable.objects.values('open__course__course_name').filter(id=id)
                couname = cn[0]['open__course__course_name']
                ScoreTable.objects.filter(id=id).update(score=sc,
                                            GradePoint=(sc/10)-5)
                writeinfo = OpenTable.objects.values('course__credit',
                                                     'course__CourseNature',
                                                     'course__course_id',
                                                     'teacher__tea_name',
                                                     'semester',
                                                     'year',
                                                     'scoretable__score',
                                                     'scoretable__GradePoint',
                                                     'scoretable__student__stu_id',
                                                     'scoretable__student__stu_name',
                                                     'scoretable__student__stu_class',
                                                     'course__course_name',
                                                     'scoretable__id'
                                                     ).filter(course__course_name=couname)

                courseinfo = CourseTable.objects.filter(opentable__teacher__tea_id=teaid)
                return render(request, 'tea_xsScore.html',
                              {'inifo': session(request), "writeinfo": writeinfo, 'courseinfo': courseinfo})
            else:
                return HttpResponse("请输入合法的分数（0<=分数<=100）")

    else:
        return HttpResponse("还未到录成绩的时候哦！")


# 导出excel数据
def excel_export(request,id):
    """导出excel表格"""
    n = ScoreTable.objects.values('open__course__course_name').filter(id=id)
    cn = n[0]['open__course__course_name']
    list_obj = OpenTable.objects.values('course__credit',
                                         'course__CourseNature',
                                         'course__course_id',
                                         'teacher__tea_name',
                                         'semester',
                                         'year',
                                         'scoretable__score',
                                         'scoretable__GradePoint',
                                         'scoretable__student__stu_id',
                                         'scoretable__student__stu_name',
                                         'scoretable__student__stu_class',
                                         'course__course_name',
                                         'scoretable__id'
                                         ).filter(course__course_name=cn)

    # print(list_obj)
    if list_obj:
        # 创建工作薄
        ws = Workbook(encoding="UTF-8")
        w = ws.add_sheet(u'数据报表第一页')
        w.write(0, 0, '学年')
        w.write(0, 1, u'学期')
        w.write(0, 2, u'姓名')
        w.write(0, 3, u'学号')
        w.write(0, 4, u'班级')
        w.write(0, 5, u'课程代码')
        w.write(0, 6, u'课程名称')
        w.write(0, 7, u'课程性质')
        w.write(0, 8, u'学分')
        w.write(0, 9, u'绩点')
        w.write(0, 10, u'任课教师')
        w.write(0, 11, u'成绩')

        # 写入数据
        excel_row = 1
        for obj in list_obj:
            print(obj)
            w.write(excel_row, 0, obj['year'])
            w.write(excel_row, 1, obj['semester'])
            w.write(excel_row, 2, obj['scoretable__student__stu_name'])
            w.write(excel_row, 3, obj['scoretable__student__stu_id'])
            w.write(excel_row, 4, obj['scoretable__student__stu_class'])
            w.write(excel_row, 5, obj['course__course_id'])
            w.write(excel_row, 6, obj['course__course_name'])
            w.write(excel_row, 7, obj['course__CourseNature'])
            w.write(excel_row, 8, obj['course__credit'])
            w.write(excel_row, 9, obj['scoretable__GradePoint'])
            w.write(excel_row, 10, obj['teacher__tea_name'])
            w.write(excel_row, 11, obj['scoretable__score'])

            excel_row += 1
            # 检测文件是否存在

        # exist_file = os.path.exists("stu_scoreinfo.xls")
        # if exist_file:
        #     os.remove(r"stu_scoreinfo.xls")
        # ws.save("scinfo.xls")
        ############################
        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(list_obj[0]['course__course_id']+'.xls')
        response.write(sio.getvalue())
        return response


@login_required
def tea_studentcf(request):
    puninfo = PunishmentTable.objects.all()
    return render(request, 'tea_xswjgl.html', {'inifo': session(request),"puninfo":puninfo})


@login_required
@csrf_exempt
def tea_cxPunishment(request,id):
    qxobj = JurisdictionTable.objects.values('IsCancel')
    qx = qxobj[0]['IsCancel']
    us = request.session['user']
    teaid = us['username']
    posittionobj = TeacherTable.objects.values('position').filter(tea_id=teaid)
    posittion = posittionobj[0]['position']
    print(qx,posittion)
    if qx == True and posittion == '2':
        PunishmentTable.objects.filter(id=id).update(iscancel=True)
        return tea_studentcf(request)
    else:
        return HttpResponse('您暂时没有权限处理违纪哦！')


@login_required
def tea_studentLeave(request):#管理请假
    leaveinfo = LeaveTable.objects.all()
    return render(request, 'tea_stuleave.html', {'inifo': session(request),'leaveinfo':leaveinfo})




@login_required
@csrf_exempt
def tea_examineLeave(request,id):#审核请假
    qxobj = JurisdictionTable.objects.values('IsLeave')
    qx = qxobj[0]['IsLeave']
    us = request.session['user']
    teaid = us['username']
    teaobj = TeacherTable.objects.values('tea_name','position').filter(tea_id=teaid)
    if qx == True and teaobj[0]['position'] == '1':
        result = request.POST.get('reason')
        if 'reject' in request.POST:
            LeaveTable.objects.filter(id=id).update(shtype=1,result=result,isAgree=False,agreeTeacher=teaobj[0]['tea_name'])
            return tea_studentLeave(request)
        else:

            LeaveTable.objects.filter(id=id).update(shtype=1, result=result, isAgree=True,
                                                    agreeTeacher=teaobj[0]['tea_name'])
            return tea_studentLeave(request)
    else:
        return HttpResponse('您暂时无法审核请假哦！')




@login_required
def tea_myClass(request): #查看任课表
    courseinfo = []
    us = request.session['user']
    teaid = us['username']
    course = CourseTable.objects.values_list('course_name','course_id','time','adress').filter(opentable__teacher__tea_id=teaid)
    for cou in course:
        coursedict = {
            'coursename':'',
            'courseid':'',
            'time':'',
            'adress':'',
        }
        coursedict['coursename'] = cou[0]
        coursedict['courseid'] = cou[1]
        coursedict['time'] = cou[2]
        coursedict['adress'] = cou[3]
        courseinfo.append(coursedict)
    return render(request, 'tea_rkb.html', {'inifo': session(request),'courseinfo':courseinfo})




@login_required
def tea_notice(request): #通知
    noticeinfo = NoticeTable.objects.all()
    return render(request, 'tea_notice.html', {'inifo': session(request), "noticeinfo": noticeinfo})
import json
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,HttpResponse
from .models import *
from apps.login.views import login_required

# Create your views here.
def test(request):
    return render(request, 'stu_cjgl.html')


def session(request):
    us = request.session['user']
    stuid = us['username']
    inifo = StudentTable.objects.filter(stu_id=stuid)
    return inifo

@login_required
def stu_index(request):  # 首页

    return render(request, 'index.html', {'inifo': session(request)})

@login_required
def stu_mssg(request):  # 个人信息

    return render(request, 'stu_mymssg.html', {'stumssg': session(request)})

@login_required
def stu_score(request):  # 成绩管理

    return render(request, 'stu_cjgl.html', {'stumssg': session(request)})



@login_required
@csrf_exempt
def stu_queryScore(request):  # 查询成绩
    us = request.session['user']
    stuid = us['username']
    year = json.loads(request.body.decode('utf-8'))['studyYear']
    sem = json.loads(request.body.decode('utf-8'))['studyTime']
    score = []
    stuk = ScoreTable.objects.values('open').filter(student__stu_id=stuid)
    # print(stuk)
    try:
        for i in list(stuk):
            scoredict = {
                'year': year,
                'sem': sem,
                'course_name': '',
                'course_id': '',
                'CourseNature': '',
                'credit': '',
                'score': 0,
                'GradePoint': '',
                'teacher': ''
            }
            openid = i['open']
            course = OpenTable.objects.values('course').filter(year=year, semester=sem, id=openid)
            sco = ScoreTable.objects.values('score').filter(open__course_id=openid)
            grp = ScoreTable.objects.values('GradePoint').filter(open__course_id=openid)
            tea = OpenTable.objects.values('teacher').filter(year=year, semester=sem, id=openid)
            courseid = course[0]['course']
            cname = CourseTable.objects.values('course_name').filter(id=courseid)
            clist = CourseTable.objects.values_list('course_id', 'CourseNature', 'credit').filter(id=courseid)
            tid = tea[0]['teacher']
            tname = TeacherTable.objects.values('tea_name').filter(id=tid)

            scoredict['course_name'] = cname[0]['course_name']
            scoredict['course_id'] = clist[0][0]
            scoredict['CourseNature'] = clist[0][1]
            scoredict['credit'] = clist[0][2]
            scoredict['score'] = sco[0]['score']
            scoredict['GradePoint'] = grp[0]['GradePoint']
            scoredict['teacher'] = tname[0]['tea_name']
            # print(scoredict)
            score.append(scoredict)

    except Exception as f:
        print(f)

    # print(score)

    return JsonResponse(score, safe=False)


@login_required
def stu_choiceCourse(request):  # 选课
    choiceinfo = []
    courseinfo = []

    us = request.session['user']
    stuid = us['username']

    cour = OpenTable.objects.values_list('id', 'course__course_name', 'course__course_id',
                                         'course__CourseNature', 'course__credit',
                                         'course__time', 'course__adress', 'teacher__tea_name')
    for course in cour:
        coursedict = {
            'id': 0,
            'coursename': '',
            'courseid': '',
            'coursenature': '',
            'credit': '',
            'time': '',
            'adress': '',
            'teacher': ''
        }

        coursedict['id'] = course[0]
        coursedict['coursename'] = course[1]
        coursedict['courseid'] = course[2]
        coursedict['coursenature'] = course[3]
        coursedict['credit'] = course[4]
        coursedict['time'] = course[5]
        coursedict['adress'] = course[6]
        coursedict['teacher'] = course[7]
        courseinfo.append(coursedict)

    choice = OpenTable.objects.values_list('id', 'course__course_name', 'course__course_id',
                                           'course__CourseNature', 'course__credit',
                                           'course__time', 'course__adress', 'teacher__tea_name').filter(
        scoretable__student__stu_id=stuid)

    # cou = OpenTable.objects.values('course')
    for choicecourse in choice:
        choicedict = {
            'id': 0,
            'coursename': '',
            'courseid': '',
            'coursenature': '',
            'credit': '',
            'time': '',
            'adress': '',
            'teacher': ''
        }

        choicedict['id'] = choicecourse[0]
        choicedict['coursename'] = choicecourse[1]
        choicedict['courseid'] = choicecourse[2]
        choicedict['coursenature'] = choicecourse[3]
        choicedict['credit'] = choicecourse[4]
        choicedict['time'] = choicecourse[5]
        choicedict['adress'] = choicecourse[6]
        choicedict['teacher'] = choicecourse[7]
        choiceinfo.append(choicedict)

    return render(request, 'stu_zxxk.html',
                  {'stumssg': session(request), 'courseinfo': courseinfo, 'choiceinfo': choiceinfo})

@login_required
@csrf_exempt
def stu_OnlineCourse(request, id):
    if request.method == 'POST':
        qxobj = JurisdictionTable.objects.values('IsChoice')
        qx = qxobj[0]['IsChoice']

        if qx:
            us = request.session['user']
            stuid = us['username']
            sid = StudentTable.objects.values('id').filter(stu_id=stuid)

            if 'choice' in request.POST: #选择课程
                pd = ScoreTable.objects.filter(student__stu_id=stuid, open_id=id)

                if len(pd) != 0:
                   return stu_choiceCourse(request)

                else:
                    ScoreTable.objects.create(student_id=sid[0]['id'], open_id=id, score=0, GradePoint='0')
                    return stu_choiceCourse(request)
            else: #删除课程
                mssg = ScoreTable.objects.filter(open_id=id, student__stu_id=stuid)
                mssg.delete()
                return stu_choiceCourse(request)
        else:
            return HttpResponse('还未到选课时间哦!')
    else:
        return stu_choiceCourse(request)

@login_required
def stu_myCourse(request):  # 课表

    courseinfo = []
    us = request.session['user']
    stuid = us['username']

    op = ScoreTable.objects.values('open').filter(student__stu_id=stuid)

    for opcou in op:
        cu = OpenTable.objects.values('course').filter(id=opcou['open'])
        opcu = CourseTable.objects.filter(id=cu[0]['course'])
        courseinfo.append(opcu)

    return render(request, 'stu_grkb.html', {'stumssg': session(request), 'courseinfo': courseinfo})

@login_required
def stu_leave(request):  # 请假
    us = request.session['user']
    stuid = us['username']
    leaveinfo = LeaveTable.objects.filter(uid=stuid)
    return render(request, 'stu_qj.html', {'stumssg': session(request), 'leaveinfo': leaveinfo})

@login_required
@csrf_exempt
def Leave(request):
    us = request.session['user']
    stuid = us['username']
    name = StudentTable.objects.values('stu_name').filter(stu_id=stuid)[0]['stu_name']
    startTime = json.loads(request.body.decode('utf-8'))['startTime']
    endTime = json.loads(request.body.decode('utf-8'))['endTime']
    reason = json.loads(request.body.decode('utf-8'))['content']
    LeaveTable.objects.create(uid=stuid, uname=name, startTime=startTime, endtime=endTime, reason=reason, isAgree=False)
    leaveinfo = serializers.serialize("json", LeaveTable.objects.filter(uid=stuid))  # 序列化

    return JsonResponse(leaveinfo, safe=False)

@login_required
def stu_punishment(request):  # 违纪处分
    us = request.session['user']
    stuid = us['username']
    puninfo = PunishmentTable.objects.filter(uid=stuid)
    return render(request, 'stu_wjcf.html', {'stumssg': session(request), 'puninfo': puninfo})

@login_required
def stu_notice(request):  # 通知公告
    noticeinfo = NoticeTable.objects.all()
    return render(request, 'tzgg.html', {'stumssg': session(request), "noticeinfo": noticeinfo})


def stu_idcard(request):  # 学生证
    return render(request, 'stu_xsz.html', {'stumssg': session(request)})

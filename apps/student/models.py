from django.db import models

# # Create your models here.

from ckeditor_uploader.fields import RichTextUploadingField

# class Status(models.TextChoices):
#     SEX = '男', '女'
#     POSITIONS = '辅导员','教务处','教师'

class JurisdictionTable(models.Model):#权限

    IsAddScore = models.BooleanField(verbose_name="是否可以录入成绩",default=False)
    IsModify = models.BooleanField(verbose_name="是否可以修改学生信息",default=False)
    IsCancel = models.BooleanField(verbose_name="是否可以管理违纪",default=False)
    IsLeave = models.BooleanField(verbose_name="是否可以审核请假",default=True)
    IsChoice = models.BooleanField(verbose_name="是否可以选课",default=False)
    class Meta:
        db_table="JurisdictionTable"
        verbose_name = '权限管理'
        verbose_name_plural = '权限管理'

class CollegeTable(models.Model):  # 院系表
    college_id = models.CharField(max_length=10, primary_key=True,verbose_name='院系号')  # 院系号
    college_name = models.CharField(max_length=20,verbose_name='名称')  # 名称
    class Meta:
        db_table="CollegeTable"
        verbose_name = '院系管理'
        verbose_name_plural = '院系管理'

    def __str__(self):
        return self.college_name

class ClassTable(models.Model):#班级表
    className = models.CharField(max_length=50,verbose_name="班级名称")
    nianJ = models.CharField(max_length=10,verbose_name="年级")
    college = models.ForeignKey(CollegeTable,on_delete=models.CASCADE,verbose_name='所属院系')

    class Meta:
        db_table = "ClassTable"
        verbose_name = '班级管理'
        verbose_name_plural = '班级管理'

    def __str__(self):
        return self.className

class StudentTable(models.Model):# 学生表
    SEX = (
        ('1', '男'),
        ('2', '女')
    )
    stu_id = models.CharField(verbose_name='学号', max_length=50, null=False)
    stu_name = models.CharField(verbose_name='姓名', max_length=50, null=False)
    sex = models.CharField(max_length=2,choices=SEX,verbose_name="性别")
    stu_class = models.ForeignKey(ClassTable,on_delete=models.CASCADE,verbose_name="班级")
    college = models.ForeignKey(CollegeTable, on_delete=models.CASCADE,verbose_name='院系')  # 院系号
    stu_email = models.CharField(verbose_name="电子邮件", max_length=100)
    stu_phone = models.CharField(verbose_name="联系方式",max_length=11)
    stu_AdmissionTime = models.DateTimeField(verbose_name='入学时间', auto_now_add=True)
    stu_adress = models.CharField(verbose_name="家庭住址",max_length=100)
    stu_birth = models.CharField(verbose_name="出生日期",max_length=100)
    stu_nation = models.CharField(verbose_name="民族",max_length=20,null=False)
    stu_PoliticalOutlook = models.CharField(verbose_name="政治面貌",max_length=20)
    stu_IdNumber = models.CharField(verbose_name="身份证号",max_length=18,null=False)
    stu_graduating = models.CharField(verbose_name="毕业中学",max_length=50)
    stu_SchoolSystem = models.CharField(verbose_name="学制",max_length=20,default="全日制大专")
    stu_schoolYear = models.CharField(verbose_name="学年",max_length=20,default="3年")

    class Meta:
        db_table = "StudentTable"
        verbose_name = '学生信息管理'
        verbose_name_plural = '学生信息管理'


    def __str__(self):
        return self.stu_id

class TeacherTable(models.Model):#教师表
    SEX = (
        ('1', '男'),
        ('2', '女')
    )
    POSITIONS = (
        ('1','辅导员'),
        ('2','教务处'),
        ('3','教师'),
        ('4','团支部书记'),
        ('5', '党支部书记'),
        ('6', '院长'),
        ('7', '副院长'),
        ('8', '校长'),
        ('9', '副校长'),
        ('10', '其他...'),
    )
    tea_id = models.CharField(verbose_name='工号',max_length=50, null=False)
    tea_name = models.CharField(verbose_name='姓名',max_length=50, null=False)
    sex = models.CharField(max_length=2, choices=SEX,verbose_name="性别")
    position = models.CharField(max_length=3,choices=POSITIONS,verbose_name="职位")
    tea_title = models.CharField(verbose_name='职称', max_length=50, null=False)
    tea_email = models.CharField(verbose_name="电子邮件", max_length=100)
    tea_phone = models.CharField(verbose_name="联系方式", max_length=11)
    tea_AdmissionTime = models.DateTimeField(verbose_name='入职时间', auto_now_add=True)
    tea_adress = models.CharField(verbose_name="家庭住址", max_length=100)
    tea_birth = models.CharField(verbose_name="出生日期", max_length=100)
    tea_nation = models.CharField(verbose_name="民族", max_length=20, null=False)
    tea_PoliticalOutlook = models.CharField(verbose_name="政治面貌", max_length=20)
    tea_IdNumber = models.CharField(verbose_name="身份证号", max_length=18, null=False)
    tea_GraduateUniversity = models.CharField(verbose_name="毕业大学", max_length=50)
    tea_education = models.CharField(verbose_name="学历", max_length=50)
    tea_major = models.CharField(verbose_name="专业", max_length=20)
    college = models.ForeignKey(CollegeTable, on_delete=models.CASCADE,verbose_name='院系')  # 院系号

    class Meta:
        db_table = "TeacherTable"
        verbose_name = '教师信息管理'
        verbose_name_plural = '教师信息管理'

    def __str__(self):
        return self.tea_name

class CourseTable(models.Model):  # 课程表
    course_id = models.CharField(verbose_name='课程代码', max_length=50, null=False)
    course_name = models.CharField(verbose_name='课程名称',max_length=50,null=False)
    CourseNature = models.CharField(verbose_name='课程性质',max_length=50,null=False)
    credit = models.CharField(verbose_name='学分',max_length=50,null=False)
    time = models.CharField(verbose_name='上课时间',max_length=50,null=False)
    adress = models.CharField(verbose_name='上课地点',max_length=50,null=False)


    class Meta:
        db_table = "CourseTable"
        verbose_name = '课程管理'
        verbose_name_plural = '课程管理'

    def __str__(self):
        return self. course_name


class OpenTable(models.Model):  # 开课表
    course = models.ForeignKey(CourseTable, on_delete=models.CASCADE,verbose_name='课程')  # 课程
    teacher = models.ForeignKey(TeacherTable, on_delete=models.CASCADE,verbose_name='教师')  # 教师
    year = models.CharField(max_length=20,verbose_name='学年')  # 学年
    semester = models.CharField(max_length=20,verbose_name='学期')  # 学期


    class Meta:
        unique_together = ("course", "teacher", "semester")

    class Meta:
        db_table = "OpenTable"
        verbose_name = '开课管理'
        verbose_name_plural = '开课管理'
    # def __str__(self):
    #     return self.year

class ScoreTable(models.Model):  # 选课表
    student = models.ForeignKey(StudentTable, on_delete=models.CASCADE,verbose_name='学号')  # 学号
    open = models.ForeignKey(OpenTable, on_delete=models.CASCADE,verbose_name='开课标识号')  # 开课标识号
    score = models.FloatField(default=0)  # 最终成绩
    GradePoint = models.CharField(verbose_name='绩点', max_length=10)
    class Meta:
        unique_together = ("student", "open")
        db_table = "ScoreTable"
        verbose_name = '选课管理'
        verbose_name_plural = '选课管理'

class NoticeTable(models.Model):   #通知公告
    title = models.CharField(verbose_name='标题', max_length=200)
    content = RichTextUploadingField(verbose_name='内容')
    time = models.DateTimeField(verbose_name='发布时间',auto_now_add=True)
    class Meta:

        db_table = "NoticeTable"
        verbose_name = '通知管理'
        verbose_name_plural = '通知管理'
    def __str__(self):
        return self. title

class LeaveTable(models.Model):   #请假
    uid = models.CharField(verbose_name='学号/工号', max_length=20)
    uname = models.CharField(verbose_name='姓名', max_length=50)
    startTime = models.CharField(verbose_name='开始时间', max_length=50)
    endtime = models.CharField(verbose_name='结束时间', max_length=50)
    reason = models.CharField(verbose_name='请假原因', max_length=500)
    isAgree = models.BooleanField(verbose_name='是否同意')
    shtype = models.IntegerField(verbose_name='审核状态',default=0)
    result = models.CharField(verbose_name='审核意见',max_length=500,default="无")
    agreeTeacher = models.CharField(verbose_name='审核人', max_length=50,default="无")
    class Meta:

        db_table = "LeaveTable"
        verbose_name = '请假管理'
        verbose_name_plural = '请假管理'
    def __str__(self):
        return self. uname

class PunishmentTable(models.Model):   #违纪处分
    uid = models.CharField(verbose_name='学号/工号', max_length=20)
    uname = models.CharField(verbose_name='姓名', max_length=50)
    createtime = models.DateTimeField(verbose_name='时间',auto_now_add=True)
    reason = models.CharField(verbose_name='违纪原因', max_length=2000)
    type = models.CharField(verbose_name='违纪类型', max_length=50)
    examine = models.CharField(verbose_name='审核', max_length=50,default='教务处')
    iscancel = models.BooleanField(verbose_name='是否取消', default=False)
    class Meta:
        db_table = "PunishmentTable"
        verbose_name = '违纪处分管理'
        verbose_name_plural = '违纪处分管理'

    def __str__(self):
        return self.uname
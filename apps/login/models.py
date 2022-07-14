from django.db import models

# Create your models here.

#用户表
class UPC_User(models.Model):
    u_uid = models.CharField(verbose_name='账号',max_length=50,null=False)
    u_password = models.CharField(verbose_name='密码',max_length=50,null=False)
    u_name = models.CharField(verbose_name='姓名',max_length=50,null=False)
    u_type = models.BooleanField(verbose_name='是否是教师',default=False)


    class Meta:
        db_table = 'UPC_User'
        verbose_name = '用户管理'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return self.u_uid
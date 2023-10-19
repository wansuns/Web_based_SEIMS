from django.db import models
# Create your models here. 数据库，类->sql语句（orm）


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name="username", max_length=64)
    password = models.CharField(verbose_name="password", max_length=128)
    limits = models.IntegerField(verbose_name="limits", choices=((0, '学生'), (1, '老师')), null=True, default=1)
    avatar = models.ImageField(verbose_name="头像", upload_to="avatars/", null=True, blank=True)
    def __str__(self):
        return self.username

class Students(models.Model):
    sid = models.IntegerField(verbose_name="学号")
    name = models.CharField(max_length=50, verbose_name='姓名')
    age = models.PositiveSmallIntegerField(verbose_name='年龄')
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')), verbose_name='性别')
    address = models.CharField(max_length=200, verbose_name='地址')
    phone = models.CharField(max_length=20, verbose_name='电话')
    email = models.EmailField(verbose_name='电子邮件')
    parent_name = models.CharField(max_length=50, verbose_name='紧急联系人姓名')
    parent_phone = models.CharField(max_length=20, verbose_name='紧急联系人电话')
    score = models.IntegerField(verbose_name="成绩")


class Teacher(models.Model):
    tid = models.IntegerField(verbose_name="教工号")
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=20, verbose_name='电话')


class ClassScore(models.Model):
    class_id = models.IntegerField(verbose_name="课程编号")
    classname = models.CharField(max_length=50, verbose_name="课程名")
    class_score = models.IntegerField(verbose_name="分数")
    sid = models.IntegerField(verbose_name="学号")






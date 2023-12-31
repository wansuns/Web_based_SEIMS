# Generated by Django 3.2.18 on 2023-05-13 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20230511_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classscore',
            name='class_id',
            field=models.IntegerField(verbose_name='课程编号'),
        ),
        migrations.AlterField(
            model_name='classscore',
            name='class_score',
            field=models.IntegerField(verbose_name='分数'),
        ),
        migrations.AlterField(
            model_name='students',
            name='score',
            field=models.IntegerField(verbose_name='成绩'),
        ),
        migrations.AlterField(
            model_name='students',
            name='sid',
            field=models.IntegerField(verbose_name='学号'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='tid',
            field=models.IntegerField(verbose_name='教工号'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='limits',
            field=models.IntegerField(choices=[(0, '学生'), (1, '老师')], null=True, verbose_name='limits'),
        ),
    ]

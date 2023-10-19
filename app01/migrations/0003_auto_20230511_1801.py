# Generated by Django 3.2.18 on 2023-05-11 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20230504_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.IntegerField(max_length=12, verbose_name='课程编号')),
                ('classname', models.CharField(max_length=50, verbose_name='课程名')),
                ('class_score', models.IntegerField(max_length=10, verbose_name='分数')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.IntegerField(max_length=12, verbose_name='学号')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('age', models.PositiveSmallIntegerField(verbose_name='年龄')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], max_length=10, verbose_name='性别')),
                ('address', models.CharField(max_length=200, verbose_name='地址')),
                ('phone', models.CharField(max_length=20, verbose_name='电话')),
                ('email', models.EmailField(max_length=254, verbose_name='电子邮件')),
                ('parent_name', models.CharField(max_length=50, verbose_name='紧急联系人姓名')),
                ('parent_phone', models.CharField(max_length=20, verbose_name='紧急联系人电话')),
                ('score', models.IntegerField(max_length=10, verbose_name='成绩')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.IntegerField(max_length=12, verbose_name='教工号')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('phone', models.CharField(max_length=20, verbose_name='电话')),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='limits',
            field=models.IntegerField(choices=[('0', 'students'), ('1', 'teacher')], max_length=10, null=True, verbose_name='limits'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=64, verbose_name='username'),
        ),
    ]

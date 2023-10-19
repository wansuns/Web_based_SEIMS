from django import forms
from .models import UserInfo, Students, ClassScore, Teacher


class MyLoginModelForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入用户名"}),
    )
    pwd = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "输入密码"}, render_value=True),
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "输入验证码"}),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', widget=forms.TextInput)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)
    limits = forms.ChoiceField(label='身份', widget=forms.RadioSelect, choices=((0, '学生'), (1, '老师')))
    avatar = forms.ImageField(label='头像', required=False)


class MyStudentsModelForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class ClassScoreForm(forms.ModelForm):
    class_id = forms.IntegerField(label="课程编号")
    classname = forms.CharField(max_length=50, label="课程名")
    class_score = forms.IntegerField(label="分数")
    sid = forms.IntegerField(label="学号")

    class Meta:
        model = ClassScore
        fields = ['class_id', 'classname', 'class_score', 'sid']

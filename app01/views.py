from django.contrib.auth.handlers.modwsgi import check_password
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from app01.models import UserInfo, Students
from app01.utils.helper import check_code
from .form import MyLoginModelForm, RegisterForm, MyStudentsModelForm
from app01.utils.encrypt import md5
from app01.utils.encrypt import EncryptionUtilWithDjango
from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.视图函数


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == 'GET':
        # pass
        #  窗口类
        form = MyLoginModelForm()
        return render(request, 'login.html', {'form': form})
    else:  # post
        form = MyLoginModelForm(data=request.POST)
        if form.is_valid():

            username = request.POST.get('username')
            pwd = request.POST.get('pwd')  # 获取用户输入的明文密码
            print(form.cleaned_data['username'], form.cleaned_data['pwd'])

            # 判断验证码是否正确
            image_code = request.session.get("image_code")
            if not image_code:
                form.add_error("code", "验证码已过期")
                return render(request, 'login.html', {"form": form})
            if image_code.upper() != form.cleaned_data['code'].upper():
                form.add_error("code", "验证码错误")
                return render(request, 'login.html', {"form": form})

            # 验证码正确，去数据库校验用户名和密码
            pwd = md5(pwd)
            obj_user = UserInfo.objects.filter(username=username, password=pwd).first()  # 获取用户信息

            if obj_user:  # 使用check_password()方法进行密码验证
                request.session['id'] = obj_user.id
                return redirect('slist')
            else:
                error = '用户名或密码不正确'
                return render(request, 'login.html', {'form': form, 'error': error})

        else:
            return render(request, 'login.html', {'form': form})


def image_code(request):
    print('enter image_code')
    # 1.生成图片
    image_object, code_str = check_code()

    # 2.图片内容返回写入内存，从内存读取并返回
    from io import BytesIO
    stream = BytesIO()
    image_object.save(stream, 'png')

    # 3.图片的内容写入session中 + 60s
    request.session['image_code'] = code_str
    request.session.set_expiry(60)
    return HttpResponse(stream.getvalue())


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = request.FILES.get('avatar')
            # 加密密码
            password = md5(form.cleaned_data['password'])
            if avatar:
                fs = FileSystemStorage(location='media/avatars')
                filename = fs.save(avatar.name, avatar)
                avatar_url = fs.url(filename)
            else:
                avatar_url = None
            # 创建用户
            user = UserInfo.objects.create(
                username=form.cleaned_data['username'],
                password=password,
                limits=form.cleaned_data['limits'],
                avatar=avatar_url
            )
            # 跳转到登录页面
            return redirect('login')
        else:
            print(request.POST)
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def stu_list(request):
    student_list = Students.objects.all()
    paginator = Paginator(student_list, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'stu_list.html', {'page_obj': page_obj})
    # return render(request, 'stu_list.html', {"students": student_list})


def stu_add(request):
    if request.method == 'GET':
        form = MyStudentsModelForm()
        return render(request, 'stu_add.html', {'form': form})
    else:  # post请求
        form = MyStudentsModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            print('save success!')
            return redirect('slist')
        else:
            print('验证出错！', form.errors)
            return render(request, 'stu_add.html', {'form': form})


def stu_mod(request, sid):
    stu_obj = Students.objects.filter(sid=sid).first()
    if request.method == 'GET':
        form = MyStudentsModelForm(instance=stu_obj)
        return render(request, 'stu_mod.html', {'form': form})
    form = MyStudentsModelForm(data=request.POST, instance=stu_obj)
    if form.is_valid():
        form.save()
        return redirect('slist')
    else:
        return render(request, 'stu_mod.html', {'form': form})


def stu_del(request, sid):
    Students.objects.filter(sid=sid).delete()
    return redirect('slist')


def stu_search(request):
    item = request.GET.get('item', '')
    query = request.GET.get('query', '')
    page_number = request.GET.get('page', 1)
    # if 有值会执行第一个分支，永远不会进入第二个分支，所以and不能放中间
    if item and query:
        students_list = Students.objects.filter(Q(name__icontains=item) & Q(sid__icontains=query))
    elif item:
        students_list = Students.objects.filter(Q(name__icontains=item))
        request.session.pop('query', None)
    elif query:
        students_list = Students.objects.filter(Q(sid__icontains=query))
    else:
        students_list = Students.objects.all()

    paginator = Paginator(students_list, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'form': MyStudentsModelForm(),
        'page_obj': page_obj,
        'item': item,
        'query': query
    }
    return render(request, 'stu_search.html', context)



import cv2
from django.shortcuts import render
from django.http import HttpResponse
import numpy as np

def detect_face(request):
    if request.method == 'POST' and request.FILES['image_file']:
        image_file = request.FILES['image_file']
        img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        img = cv2.resize(img, (800, 600))
        # 加载人脸检测器
        face_cascade = cv2.CascadeClassifier('E:/pythonfiles/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

        # 将图片转换为灰度图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 检测人脸
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # 在人脸上绘制边界框
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 将带有边界框的图片转换为 JPEG 格式，并作为响应返回
        _, jpeg_data = cv2.imencode('.jpg', img)
        response = HttpResponse(jpeg_data.tobytes(), content_type='image/jpeg')
        return response
    return render(request, 'model.html', {'result': None})


from .models import ClassScore


def course(request):
    courses =ClassScore.objects.all()

    return render(request, 'course.html', {'courses': courses})




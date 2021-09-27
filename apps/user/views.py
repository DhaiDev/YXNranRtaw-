from functools import wraps

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from apps.user.models import UserInfo


def check_login(func):
    @wraps(func)
    def inner(obj, request, *args, **kwargs):
        ret = request.session.get("is_login")
        # 1. 获取cookie中的随机字符串
        # 2. 根据随机字符串去数据库取 session_data --> 解密 --> 反序列化成字典
        # 3. 在字典里面 根据 is_login 取具体的数据

        if ret == "1":
            # 已经登录，继续执行
            return func(obj, request, *args, **kwargs)
        # 没有登录过
        else:
            # ** 即使登录成功也只能跳转到home页面，现在通过在URL中加上next指定跳转的页面
            # 获取当前访问的URL
            next_url = request.path_info
            # , content = {'error': 'Please Login First !'}
            return redirect(f"/user/login/?next={next_url}")

    return inner


def logout(request):
    # 只删除session数据
    # request.session.delete()

    # 删除session数据和cookie
    request.session.flush()

    return redirect("/")




class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        next_url = request.GET.get("next")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserInfo.objects.filter(username=username).first()
        error = {
            'error': 'User Not Found!',
        }
        if user:
            if check_password(password=password, encoded=user.password):
                request.session["is_login"] = "1"
                request.session["name"] = username

                if next_url:
                    rep = redirect(next_url)
                else:
                    rep = redirect("/")
                return rep
            else:
                error['error'] = 'Better check your username or password !'

        return render(request, 'login.html', context=error)


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        matrix = request.POST.get('matrix')
        email = request.POST.get('matrix')
        error = {
            'error': 'User is Exist ! Please Sign In',
        }
        if 12 >= len(username) >= 6:
            if password1 == password2 and 26 >= len(password1) >= 6:
                if UserInfo.objects.filter(username=username).first():
                    return render(request, '404.html', context=error)
                if matrix == 'administor':
                    user = UserInfo(username=username, password=make_password(password=password1), email=email,
                                    is_staff=True)
                else:
                    user = UserInfo(username=username, password=make_password(password=password1), email=email)
                user.save()
                # 设置session
                request.session["is_login"] = "1"
                request.session["name"] = username
                return redirect("/", content={'username': username})
            else:
                error['error'] = 'Username or Password Error , Please Check Up !  '
                return render(request, '404.html', context=error)
        error['error'] = 'Username so Short !'
        return render(request, '404.html', context=error)

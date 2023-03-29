import random
import uuid

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app01.models import user, disposition
from django.core import serializers
import json
import re


# 用户管理API

# 后台创建root
def sign_up_root(request):
    user1 = user(user_id="123456", user_name='root', permission=1)
    user1.save()
    return HttpResponse("<p>root添加成功！</p>")

# 创建系统管理员
@require_http_methods(["GET"])
def create(request):
    response = {}
    un = request.GET.get('user_name')
    pwd = request.GET.get('password')
    is_superuser = request.GET.get('is_superuser')
    try:

        User.objects.create_user(
            username=un,
            password=pwd,
            is_superuser=is_superuser
        )
        response['msg'] = '创建成功'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

# 用户登录
class LoginView(View):

    def post(self, request):

        response = {}

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(password)
        # 验证如果用户不为空
        if user is not None:
            # login方法登录
            if request.user == user:
                response['msg'] = username + ' ' + '用户已登录'
                response['error_num'] = 1
            else:
                login(request, user)
            # 返回登录成功信息
                response['msg'] = username + ' ' + '登录成功'
                response['error_num'] = 0
            return JsonResponse(response)
        else:
            # 返回登录失败信息
            response['msg'] = '登录失败'
            response['error_num'] = 1
            return JsonResponse(response)

# 用户登出
class LogoutView(View):

    def get(self, request):
        user1 = request.user
        response = {}
        if user1:
            logout(request)
            response['msg'] = user1.username + ' ' + '登出成功'
            response['error_num'] = 0
        else:
            response['msg'] = '无用户'
            response['error_num'] = 1

        return JsonResponse(response)

# 删除用户
class DeleteUserView(View):

    def post(self, request):

        response = {}

        #user1 = User.objects.get(id=request.POST.get('user_id'))
        user1 = User.objects.get(username=request.POST.get('username'))

        if user1.id == request.user.id:
            response['msg'] = '您可以通过注销账号删除自己的账号！'
            response['error_num'] = 1
        else:
            if user1.is_superuser == 1:
                response['msg'] = '无删除权限！'
                response['error_num'] = 2
            else:
                user1.delete()
                response['msg'] = '删除成功'
                response['error_num'] = 0

        return JsonResponse(response)

# 展示用户列表
class ListUserView(View):

    def get(self, request):

        user = User.objects.all().values('username','is_superuser')
        return JsonResponse(list(user), safe=False)

# 药品/疫苗管理API
# 创建药品/疫苗
class CreateDispositionView(View):

    def post(self, request):

        name = request.POST.get('name')
        intro = request.POST.get('intro')
        price = request.POST.get('price')

        id = str(uuid.uuid4())[:8]

        dispositon1 = disposition.objects.create(
            disposition_id=id,
            disposition_name = name,
            disposition_price = price,
            introduction = intro
        )

        return JsonResponse({'msg': '创建成功','error_num': 0})




# 删除药品/疫苗
class DeleteDispositionView(View):

    def post(self, request):

        response = {}
        name = request.POST.get('name')
        print(name)
        disposition1 = disposition.objects.get(disposition_name=name)
        if not disposition1 == None:
            disposition1.delete()
            response['msg'] = '删除成功'
            response['error_num'] = 0

        else:
            response['msg'] = '该药品不存在'
            response['error_num'] = 1

        return JsonResponse(response)

# 展示药品/疫苗
class ListDispositionView(View):

    def get(self, request):
        disposition1 = disposition.objects.all().values(
            'disposition_name','introduction','disposition_price')
        return JsonResponse(list(disposition1), safe=False)

# 修改药品/疫苗



# 化验项目管理API
# 创建
# 删除
# 展示
# 修改



# 病种病例管理API
# 创建
# 删除
# 展示
# 修改

# 创建
# 删除
# 展示
# 修改


# 测试管理API
# 考题相关API
# 创建
# 删除
# 展示
# 查看
# 修改
# 查看管理
# 增加管理
# 删除管理

# 试卷相关API
# 创建
# 删除
# 展示
# 查看
# 修改
# 添加考题
# 删除考题
# 考题排序
# 查看管理
# 增加管理
# 删除管理

# 测试相关API
# 创建
# 删除
# 展示
# 查看
# 修改
# 查看管理
# 增加管理
# 删除管理
# 设置考生

# 成绩相关API
# 展示
# 评分



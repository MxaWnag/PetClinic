import random

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app01.models import user
from django.core import serializers
import json
import re


# Create your views here.
def sign_up_root(request):
    user1 = user(user_id="123456", user_name='root', permission=1)
    user1.save()
    return HttpResponse("<p>root添加成功！</p>")


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




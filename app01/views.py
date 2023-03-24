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
    try:

        User.objects.create_user(
            username=request.GET.get('user_name'),
            password=request.GET.get('password')
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
            if user.is_active:
                response['msg'] = username + ' ' + '用户已登录'
                response['error_num'] = 1
            else:
                login(request, user)
            # 返回登录成功信息
                response['msg'] = username + ' ' + '登陆成功'
                response['error_num'] = 0
            return JsonResponse(response)
        else:
            # 返回登录失败信息
            response['msg'] = '登陆失败'
            response['error_num'] = 1
            return JsonResponse(response)


class LogoutView(View):

    def get(self, request):
        logout(request=request)
        response = {}
        response['msg'] = '登出成功'
        response['error_num'] = 0

        return JsonResponse(response)

class DeleteUserView(View):

    @login_required(login_url='/login/')
    def post(self, request):
        user1 = User.objects.get()

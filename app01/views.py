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
from app01.models import user, disposition, project, disease, case
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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

        # user1 = User.objects.get(id=request.POST.get('user_id'))
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
        user = User.objects.all().values('username', 'is_superuser')
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
            disposition_name=name,
            disposition_price=price,
            introduction=intro
        )
        dispositon1.save()

        return JsonResponse({'msg': '创建成功', 'error_num': 0})


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
            'disposition_name', 'introduction', 'disposition_price')
        if disposition.objects.all().exists():
            return JsonResponse(list(disposition1), safe=False)
        else:
            return JsonResponse({'msg': '暂无药品/疫苗', 'error_num': 1})


# 修改药品/疫苗
class EditDispositionView(View):

    def post(self, request):
        id = request.POST.get('id')

        name = request.POST.get('name')
        intro = request.POST.get('intro')
        price = request.POST.get('price')

        disposition1 = disposition.objects.get(disposition_id=id)
        disposition1.disposition_name = name
        disposition1.disposition_price = price
        disposition1.introduction = intro
        disposition1.save()

        return JsonResponse({'msg': '修改成功', 'error_num': 0})


# 化验项目管理API
# 创建
class CreateProjectView(View):

    def post(self, request):
        name = request.POST.get('name')
        intro = request.POST.get('intro')
        price = request.POST.get('price')

        id = str(uuid.uuid4())[:8]

        project1 = project.objects.create(
            project_id=id,
            project_name=name,
            project_price=price,
            introduction=intro
        )
        project1.save()

        return JsonResponse({'msg': '创建成功', 'error_num': 0})


# 删除
class DeleteProjectView(View):

    def post(self, request):

        response = {}
        name = request.POST.get('name')
        print(name)
        project1 = project.objects.get(project_name=name)
        if not project1 == None:
            project1.delete()
            response['msg'] = '删除成功'
            response['error_num'] = 0

        else:
            response['msg'] = '该化验项目不存在'
            response['error_num'] = 1

        return JsonResponse(response)


# 展示
class ListProjectView(View):

    def get(self, request):
        project1 = project.objects.all().values(
            'project_name', 'introduction', 'project_price')
        if project.objects.all().exists():
            return JsonResponse(list(project1), safe=False)
        else:
            return JsonResponse({'msg': '暂无化验项目', 'error_num': 1})


# 修改
class EditProjectView(View):

    def post(self, request):
        id = request.POST.get('id')

        name = request.POST.get('name')
        intro = request.POST.get('intro')
        price = request.POST.get('price')

        project1 = project.objects.get(project_id=id)
        project1.project_name = name
        project1.project_price = price
        project1.introduction = intro
        project1.save()

        return JsonResponse({'msg': '修改成功', 'error_num': 0})


# 病种病例管理API
class CreateDiseaseView(View):

    def post(self, request):
        name = request.POST.get('name')
        intro = request.POST.get('intro')
        cate = request.POST.get('category')

        id = str(uuid.uuid4())[:8]

        disease1 = disease.objects.create(
            disease_id=id,
            disease_name=name,
            category=cate,
            introduction=intro
        )
        disease1.save()

        return JsonResponse({'msg': '创建成功', 'error_num': 0})


# 删除
class DeleteDiseaseView(View):

    def post(self, request):

        response = {}
        name = request.POST.get('name')
        print(name)
        disease1 = disease.objects.get(disease_name=name)
        if not disease1 == None:
            disease1.delete()
            response['msg'] = '删除成功'
            response['error_num'] = 0

        else:
            response['msg'] = '该病种不存在'
            response['error_num'] = 1

        return JsonResponse(response)


# 展示
class ListDiseaseView(View):

    def get(self, request):

        disease1 = disease.objects.all().values(
            'disease_name', 'category', 'introduction')
        if disease.objects.all().exists():
            print("**********************")
            return JsonResponse(list(disease1), safe=False)
        else:
            return JsonResponse({'msg': '暂无病种介绍', 'error_num': 1})


# 修改
class EditDiseaseView(View):

    def post(self, request):
        id = request.POST.get('id')

        name = request.POST.get('name')
        intro = request.POST.get('intro')
        cate = request.POST.get('category')

        disease1 = disease.objects.get(disease_id=id)
        disease1.disease_name = name
        disease1.category = cate
        disease1.introduction = intro
        disease1.save()

        return JsonResponse({'msg': '修改成功', 'error_num': 0})


# 创建
# class CaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = case
#         fields = [
#             'case_id', 'case_name', 'disease_id',
#             'patient_specie', 'patient_age', 'patient_weight',
#             'admission', 'admission_pic', 'admission_video',
#         ]
#
#     admission_video = serializers.ListField(
#         child=serializers.FileField(max_length=100000,
#                                     allow_empty_file=False,
#                                     use_url=False),
#         required=False)
#     admission_pic = serializers.ListField(
#         child=serializers.ImageField(max_length=100000,
#                                      allow_empty_file=False,
#                                      use_url=False),
#         required=False)
#
#
# @api_view(['POST'])
# def create_case(request):
#     serializer = CaseSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

# 删除
class DeleteCaseView(View):

    def post(self, request):

        response = {}
        name = request.POST.get('name')
        print(name)
        case1 = disease.objects.get(case_name=name)
        if case1 is not None:
            case1.delete()
            response['msg'] = '删除成功'
            response['error_num'] = 0

        else:
            response['msg'] = '该病例不存在'
            response['error_num'] = 1

        return JsonResponse(response)


# 展示
class ListCaseView(View):

    def get(self, request):

        case1 = case.objects.all().values(
            'case_name', 'patient_specie', 'admission')
        if case.objects.all().exists():
            return JsonResponse(list(case1), safe=False)
        else:
            return JsonResponse({'msg': '暂无病例介绍', 'error_num': 1})


# 查看
class ShowCaseDetailsView(View):

    def get(self, request):
        case_id = request.GET.get('case_id')
        case1 = case.objects.get(case_id=case_id).values(
            'case_name', 'disease_id',
            'patient_specie', 'patient_age', 'patient_weight',
            'admission', 'admission_pic', 'admission_video')
        if case.objects.get(case_id=case_id).exists():
            return JsonResponse(list(case1), safe=False)
        else:
            return JsonResponse({'msg': '暂无病例介绍', 'error_num': 1})
# 修改


# 测试管理API
# 考题相关API
# 创建
class CreateDiseaseView(View):

    def post(self, request):
        name = request.POST.get('name')
        intro = request.POST.get('intro')
        cate = request.POST.get('category')

        id = str(uuid.uuid4())[:8]

        disease1 = disease.objects.create(
            disease_id=id,
            disease_name=name,
            category=cate,
            introduction=intro
        )
        disease1.save()

        return JsonResponse({'msg': '创建成功', 'error_num': 0})
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

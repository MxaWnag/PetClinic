import random
import uuid
import calendar
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app01.models import disposition, project, disease, case, question, question_type, option, paper, question_paper
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
import json
import re


# 用户管理API

# 后台创建root
# def sign_up_root(request):
#     user1 = user(user_id="123456", user_name='root', permission=1)
#     user1.save()
#     return HttpResponse("<p>root添加成功！</p>")


# 创建系统管理员
@require_http_methods(["GET"])
def create(request):
    response = {}
    un = request.GET.get('user_name')
    pwd = request.GET.get('password')
    is_superuser = request.GET.get('is_superuser')  # is_superuser值为0表示系统管理员，值为1表示超级管理员
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
        print(user1.username)
        response = {}

        if user1.is_anonymous is True:
            response['msg'] = '无用户'
            response['error_num'] = 1
        else:
            logout(request)
            response['msg'] = user1.username + ' ' + '登出成功'
            response['error_num'] = 0


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
                response['msg'] = '删除成功'
                response['error_num'] = 0
            else:
                user1.delete()
                response['msg'] = '无删除权限！'
                response['error_num'] = 2


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

        disposition1 = disposition.objects.filter(disposition_name=name).count()

        if len(name) != 0:
            if disposition1 != 0:
                return JsonResponse({'msg': '该药品/疫苗已存在，请修改名称！', 'error_num': 1})
            if len(name) <= 20:
                id = str(uuid.uuid4())[:8]
                dispositon1 = disposition.objects.create(
                    disposition_id=id,
                    disposition_name=name,
                    disposition_price=price,
                    introduction=intro
                )
                dispositon1.save()

                return JsonResponse({'msg': '创建成功', 'error_num': 0})
            else:
                return JsonResponse({'msg': '药品/疫苗名称过长，请勿超过20个字符！', 'error_num': 3})
        else:
            return JsonResponse({'msg': '请完整填写药品/疫苗信息！', 'error_num': 3})


# 删除药品/疫苗
class DeleteDispositionView(View):

    def post(self, request):

        response = {}
        name = request.POST.get('name')
        print(name)
        disposition1 = disposition.objects.filter(disposition_name=name)
        if disposition1.count() != 0:
            disposition1.delete()
            response['msg'] = '删除成功'
            response['error_num'] = 0

        else:
            response['msg'] = '该药品/疫苗不存在'
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

        cnt = disposition.objects.filter(disposition_id=id).count()
        print(cnt)
        if cnt != 0:
            disposition1 = disposition.objects.get(disposition_id=id)
            if len(name) != 0:
                disposition1.disposition_name = name
            if price is not None:
                disposition1.disposition_price = price
            disposition1.introduction = intro
            disposition1.save()
            return JsonResponse({'msg': '修改成功', 'error_num': 0})
        else:
            return JsonResponse({'msg': '该药品/疫苗不存在', 'error_num': 1})




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
            'disease_id', 'disease_name', 'category', 'introduction')
        if disease.objects.all().exists():
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
class CreateCaseView(View):
    def post(self, request):
        case_id1 = str(uuid.uuid4())[:8]
        case_name1 = request.POST.get('case_name')
        disease1 = request.POST.get('disease')
        patient_specie1 = request.POST.get('specie')
        patient_age1 = request.POST.get('age')
        patient_weight1 = request.POST.get('weight')
        admission1 = request.POST.get('admission')
        checking1 = request.POST.get('checking')
        diagnostic_result1 = request.POST.get('dia_result')
        treatment1 = request.POST.get('treatment')

        case1 = case.objects.create(
            case_id=case_id1,
            case_name=case_name1,
            disease=disease.objects.get(disease_id=disease1),
            patient_specie=patient_specie1,
            patient_age=patient_age1,
            patient_weight=patient_weight1,
            admission=admission1,
            checking=checking1,
            diagnostic_result=diagnostic_result1,
            treatment=treatment1
        )
        case1.save()
        return JsonResponse({'msg': '创建成功', 'error_num': 0})
# 删除
class DeleteCaseView(View):

    def post(self, request):

        response = {}
        id = request.POST.get('id')
        case1 = case.objects.get(case_id=id)
        if case1 is not None:
            case1.delete()
            response['msg'] = '删除成功'
            response['error_num'] = 0

        else:
            response['msg'] = '该病例不存在！'
            response['error_num'] = 1

        return JsonResponse(response)


# 展示
class ListCaseView(View):

    def get(self, request):

        case1 = case.objects.all().values(
            'case_id', 'case_name', 'patient_specie', 'admission')
        if case.objects.all().exists():
            return JsonResponse(list(case1), safe=False)
        else:
            return JsonResponse({'msg': '暂无病例介绍', 'error_num': 1})

class CaseGroupView(View):
    def get(self, request):
        disease_id1 = request.GET.get('disease_id')
        case1 = case.objects.filter(disease_id=disease_id1).values(
            'case_name', 'disease__disease_name',
            'patient_specie', 'patient_age', 'patient_weight',
            'admission', 'checking', 'diagnostic_result', 'treatment'
        )
        if case.objects.filter(disease_id=disease_id1).exists():
            return JsonResponse(list(case1), safe=False)
        else:
            return JsonResponse({'msg': '暂无病例介绍', 'error_num': 1})

# 查看
class ShowCaseDetailsView(View):

    def get(self, request):
        case_id = request.GET.get('case_id')
        case1 = case.objects.filter(case_id=case_id).values(
            'case_name', 'disease__disease_name',
            'patient_specie', 'patient_age', 'patient_weight',
            'admission', 'checking','diagnostic_result','treatment')
        if case.objects.filter(case_id=case_id).exists():
            return JsonResponse(list(case1), safe=False)
        else:
            return JsonResponse({'msg': '暂无病例介绍', 'error_num': 1})
# 修改


# 测试管理API
# 考题相关API
# 创建
class CreateQuestionView(View):

    def post(self, request):
        description = request.POST.get('description')
        answer = request.POST.get('answer')
        difficulty = request.POST.get('difficulty')
        question_type1 = question_type.objects.get(type_id=request.POST.get('question_type_id'))
        disease1 = disease.objects.get(disease_id=request.POST.get('disease_id'))
        op1 = request.POST.get('op1')
        op2 = request.POST.get('op2')
        op3 = request.POST.get('op3')
        op4 = request.POST.get('op4')

        id = str(uuid.uuid4())[:8]

        question1 = question.objects.create(
            description=description,
            answer=answer,
            difficulty=difficulty,
            question_id=id,
            question_type=question_type1,
            disease_id=disease1
        )
        question1.save()

        option1 = option.objects.create(
            question=question1,
            option1=op1,
            option2=op2,
            option3=op3,
            option4=op4
        )
        option1.save()
        return JsonResponse({'msg': '创建成功', 'error_num': 0})

# 删除
class DeleteQuestionView(View):

    def post(self, request):

        response = {}
        id = request.POST.get('question_id')
        question1 = question.objects.get(question_id=id)
        option1 = option.objects.get(question_id=id)
        if not question1 == None:
            question1.delete()
            option1.delete()
            response['msg'] = '删除成功'
            response['error_num'] = 0

        else:
            response['msg'] = '该考题不存在'
            response['error_num'] = 1

        return JsonResponse(response)

# 展示
class ListQuestionView(View):

    def get(self, request):

        question1 = question.objects.all().values(
            'question_id', 'question_type','difficulty', 'description', 'disease_id__disease_name')
        if question.objects.all().exists():
            return JsonResponse(list(question1), safe=False)
        else:
            return JsonResponse({'msg': '暂无考题', 'error_num': 1})

# 查看
class ShowQuestionDetailsView(View):

    def get(self, request):
        id = request.GET.get('question_id')
        question1 = question.objects.filter(question_id=id).values(
            'question_id', 'question_type', 'description',
            'option__option1', 'option__option2', 'option__option3', 'option__option4',
            'answer', 'question_type__score')
        if question.objects.filter(question_id=id).exists():
            return JsonResponse(list(question1), safe=False)
        else:
            return JsonResponse({'msg': '暂无考题详情', 'error_num': 1})

class RandomQuestionView(View):
    def get(self, request):
        count = question.objects.all().count()
        num = random.randint(0, count-1)
        q_id = question.objects.all()[num].question_id
        question1 = question.objects.filter(question_id=q_id).values(
            'question_id', 'question_type', 'description',
            'option__option1', 'option__option2', 'option__option3', 'option__option4', 'answer')
        return JsonResponse(list(question1), safe=False)


# 试卷相关API
# 创建
class CreatePaperView(View):

    def post(self, request):
        name = request.POST.get('name')

        id = str(uuid.uuid4())[:8]
        paper1 = paper.objects.create(
            paper_id=id,
            paper_name=name,
            creator_id=0,
            creator = 'SuperUser5',
            creation_time=datetime.datetime.now()
        )
        paper1.save()

        return JsonResponse({'msg': '创建成功', 'error_num': 0})

# 删除
class DeletePaperView(View):

    def post(self, request):

        response = {}
        id = request.POST.get('paper_id')
        paper1 = paper.objects.get(paper_id=id)
        if not paper1 == None:
            paper1.delete()
            response['msg'] = '删除成功'
            response['error_num'] = 0
        else:
            response['msg'] = '该试卷不存在'
            response['error_num'] = 1

        return JsonResponse(response)

# 展示
class ListPaperView(View):

    def get(self, request):

        paper1 = paper.objects.all().values(
            'paper_id', 'paper_name', 'creator', 'creation_time')
        if paper.objects.all().exists():
            return JsonResponse(list(paper1), safe=False)
        else:
            return JsonResponse({'msg': '暂无试卷', 'error_num': 1})

# 查看
class ShowPaperDetailsView(View):
    def get(self, request):
        id = request.GET.get('paper_id')

        all_question = question_paper.objects.filter(paper_id=id).values(
            'question_id__description','question_id__option__option1', 'question_id__option__option2',
        'question_id__option__option3', 'question_id__option__option4', 'question_id__answer', 'paper_id__paper_name').order_by('question_id__question_paper__question_number')
        if question_paper.objects.filter(paper_id=id).exists():
            return JsonResponse(list(all_question), safe=False)
        else:
            return JsonResponse({'msg': '该试卷未添加考题', 'error_num': 1})
# 修改
class EditPaperView(View):

    def post(self, request):
        id = request.POST.get('paper_id')

        name = request.POST.get('paper_name')

        paper1 = paper.objects.get(paper_id=id)
        paper1.paper_name = name
        paper1.creation_time = datetime.datetime.now()
        paper1.save()

        return JsonResponse({'msg': '修改成功', 'error_num': 0})
# 添加考题
class AddQuestion2PaperView(View):

    def post(self, request):

        id = str(uuid.uuid4())[:8]
        question_id1 = request.POST.get('question_id')
        paper_id1 = request.POST.get('paper_id')
        num = request.POST.get('number')


        qp1 = question_paper.objects.create(
            qp_id=id,
            question_id=question.objects.get(question_id=question_id1),
            paper_id=paper.objects.get(paper_id=paper_id1),
            question_number=num
        )
        qp1.save()
        return JsonResponse({'msg': '创建成功', 'error_num': 0})


# 删除考题
class DeleteQuestionfromPaperView(View):

    def post(self, request):

        response = {}
        id = request.POST.get('qp_id')
        qp1 = question_paper.objects.get(qp_id=id)
        if not qp1 == None:
            qp1.delete()
            response['msg'] = '删除成功'
            response['error_num'] = 0

        else:
            response['msg'] = '该考题不存在'
            response['error_num'] = 1

        return JsonResponse(response)
# 考题排序



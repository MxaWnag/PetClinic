"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('root/', views.sign_up_root),
    path('create/', views.create),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('deleteuser/', views.DeleteUserView.as_view()),
    path('users/', views.ListUserView.as_view()),
    path('createDisposition/', views.CreateDispositionView.as_view()),
    path('deleteDisposition/', views.DeleteDispositionView.as_view()),
    path('listDisposition/', views.ListDispositionView.as_view()),
    path('editDisposition/', views.EditDispositionView.as_view()),
    path('createProject/', views.CreateProjectView.as_view()),
    path('deleteProject/', views.DeleteProjectView.as_view()),
    path('listProject/', views.ListProjectView.as_view()),
    path('editProject/', views.EditProjectView.as_view()),
    path('createDisease/', views.CreateDiseaseView.as_view()),
    path('deleteDisease/', views.DeleteDiseaseView.as_view()),
    path('listDisease/', views.ListDiseaseView.as_view()),
    path('editDisease/', views.EditDiseaseView.as_view()),
    # path('createCase/', views.create_case),
    path('deleteCase/', views.DeleteCaseView.as_view()),
    path('listCase/', views.ListCaseView.as_view()),
    path('showCaseDetails/', views.ShowCaseDetailsView.as_view()),
    path('createQuestion/', views.CreateQuestionView.as_view()),
    path('deleteQuestion/', views.DeleteQuestionView.as_view()),
    path('listQuestion/', views.ListQuestionView.as_view()),
    path('showQuestionDetails/', views.ShowQuestionDetailsView.as_view()),
    #怎么更新不上呢
    #怎么会这样呢

]

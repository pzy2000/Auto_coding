"""online_judge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import path
from judge.views import (
    display_problems,
    problem_detail,
    submit,
    show_code,
    add_problem,
    add_testcase,
    del_prob
)

from users.views import (
    register,
    login,
    logout
)

urlpatterns = [
    path('', RedirectView.as_view(url='problem/', permanent=False), name='Home'),
    path('admin/', admin.site.urls),
    path('problem/',display_problems,name='problem_page'),
    path('problem/<int:prob_id>/',problem_detail,name='detail_problem'),
    path('problem/<int:prob_id>/submission/',submit,name='past_submissions'),
    path('problem/<int:prob_id>/submission/code/<int:submission_id>/',show_code,name='show_past_code'),
    path('problem/add/', add_problem, name = 'add_problem'),
    path('problem/addtest/<int:prob_id>/', add_testcase, name = 'add_testcase'),
    path('problem/delete/<int:prob_id>/', del_prob, name = 'delete_prob'),
    path('user/login/', login, name = 'user_login'),
    path('user/register/', register, name = 'user_register'),
    path('user/logout/', logout, name = 'user_logout'),
]

from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
# Create your views here.
from rbac.models import *
import re

from rbac.service.register_rbac import rbac_login


def user(request):
    user_list = User.objects.all()
    return render(request, 'user.html', locals())






def login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username,password=password).first()
        print(user,username,password)
        if user:
            rbac_login(request,user)
            return redirect('/user/')
    return render(request,'login.html')


def useradd(request):

    return HttpResponse('useradd...')

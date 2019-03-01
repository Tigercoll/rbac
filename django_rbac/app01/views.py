from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
# Create your views here.
from rbac.models import *
import re

from rbac.service.register_rbac import rbac_login

# 新增一个类 用于判断用户是否有这个操作权限
class Permissions(object):
    #  action_list = [(1,'add'),(2,'delete'),(3,'update'),(4,'select')]
    def __init__(self,actions):
        self.actions=actions
    def add(self):
        return 1 in self.actions
    def delete(self):
        return 2in self.actions
    def update(self):
        return 3 in self.actions
    def select(self):
        return 4 in self.actions

def user(request):
    permission=Permissions(request.actions)
    get_list = User.objects.all()
    print(get_list)
    print(request.actions)
    return render(request, 'user.html', locals())


def permission(request):
    per = Permissions(request.actions)
    get_list = Permission.objects.all()
    return render(request, 'permissions.html', locals())


def roles(request):
    per = Permissions(request.actions)
    get_list = Roles.objects.all()
    return render(request, 'roles.html', locals())


def login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username,password=password).first()
        print(user,username,password)
        if user:
            # 注册rbac权限
            rbac_login(request,user)
            return redirect('/user/')
    return render(request,'login.html')


def useradd(request):

    return HttpResponse('useradd...')

## RBAC(**Role-based access control**)

基于角色的权限访问控制（Role-Based Access Control）作为传统访问控制（自主访问，强制访问）的有前景的代替受到广泛的关注。在RBAC中，权限与角色相关联，用户通过成为适当角色的成员而得到这些角色的权限。这就极大地简化了权限的管理。在一个组织中，角色是为了完成各种工作而创造，用户则依据它的责任和资格来被指派相应的角色，用户可以很容易地从一个角色被指派到另一个角色。角色可依新的需求和系统的合并而赋予新的权限，而权限也可根据需要而从某角色中回收。角色与角色的关系可以建立起来以囊括更广泛的客观情况。(来自百度百科)

我们先来看张图:

![](https://github.com/Tigercoll/my_picturelib/raw/master/rbac/1.png)

从上图我们可以看出，ACL是用户和权限直接关系的，RBAC则是通过角色间接关联用户和权限的。所以角色是RBAC系统的一个重要属性

我们要实现的功能就是1,用户管理,2,角色管理,3权限管理.

![](https://github.com/Tigercoll/my_picturelib/raw/master/rbac/2.png)

### 设计表

```python
from django.db import models

# Create your models here.

class  User(models.Model):
    """用户表"""
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=37,verbose_name='密码')
    roles = models.ManyToManyField(to='Roles')
    class Meta:
        verbose_name='用户表'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.username

class Roles(models.Model):
    """角色表"""
    title = models.CharField(max_length=37,verbose_name='角色名称')
    permission = models.ManyToManyField(to='Permission')
    class Meta:
        verbose_name='角色表'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title
class Permission(models.Model):
    """权限表"""
    title = models.CharField(max_length=37,verbose_name='权限名')
    url = models.CharField(max_length=37,verbose_name='链接')

    class Meta:
        verbose_name='权限表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title
```

用户与角色关联,角色与权限关联,用户与权限之间没有直接联系.

```python
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
```

```python
# 注册权限url列表到session

def rbac_login(request,user):
    permission_list = []
    request.session['user_id'] = user.pk
    permissions = user.roles.all().values("permission__url").distinct()
    for permission in permissions:
        permission_list.append(permission['permission__url'])
    request.session['permission_list'] = permission_list
```

将权限注册到session

由于每个访问都需要校验一遍是否有权限,所以将rbac写入中间件

```python
# rbac 中间件

import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import  HttpResponse,redirect

class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url_path = request.path_info

        # 白名单 white_list 要加斜线,
        white_list = ['/login/',]

        permission_list = request.session.get('permission_list',[])

        for white_url in white_list:
            white_url = '^%s$'%white_url
            ret = re.match(white_url,url_path)
            if ret :
                return None

        # 是否登录
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("/login/")

        # 检验权限
        for permission in permission_list:
            permission = '^%s$' % permission
            ret = re.match(permission, url_path)
            if ret:
                return None
        # 这里可以扩展到新的网页
        return HttpResponse('没有权限')
```

基本熟悉了rbac概念后可以轻松完成.

源码已放到[github](https://github.com/Tigercoll/rbac)上

欢迎各位指教




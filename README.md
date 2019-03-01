## RBAC扩展

上次我们做了一个简易的RBAC 模型.但是这样完全不能满足我们的需求,所以这次扩展了很多

在权限表里新增两个字段,新增一张权限组表 (rbac/models.py):

```python
class Permission(models.Model):
    """权限表"""
    title = models.CharField(max_length=37,verbose_name='权限名')
    url = models.CharField(max_length=37,verbose_name='链接')
    action_list = [(1,'add'),(2,'delete'),(3,'update'),(4,'select')]
    action = models.IntegerField(choices=action_list,verbose_name='动作',default=4)
    group =models.ForeignKey(to='PermissionGroup',on_delete=models.CASCADE,default='1')
    class Meta:
        verbose_name='权限表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title

class PermissionGroup(models.Model):
    title = models.CharField(max_length=32,verbose_name='权限组名')

    class Meta:
        verbose_name = '权限组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
```

这样可以使权限更细分化,方便使用

重写RBAC注册(rbac/service/register_rbac.py):

```python
# 注册权限url列表到session
'''
def rbac_login(request,user):
    permission_list = []
    request.session['user_id'] = user.pk
    permissions = user.roles.all().values("permission__url").distinct()
    for permission in permissions:
        permission_list.append(permission['permission__url'])
    request.session['permission_list'] = permission_list
'''
def rbac_login(request,user):
    # 权限字典 如:{'权限管理': {'urls': ['/permission/',  '/permission/update/(/d+)'], 'actions': [1, 4, 2, 3]}, }

    permission_dict = {}
    # 菜单列表 如:[['用户管理', '/user/'], ['角色管理', '/roles/'], ['权限管理', '/permission/']]
    menu_list = []
    
    request.session['user_id'] = user.pk
    # 获取 权限url,权限组名,权限动作
    permissions = user.roles.all().values("permission__url","permission__group_id__title","permission__action").distinct()
    
    for permission in permissions:
        group_title = permission['permission__group_id__title']
        if group_title in permission_dict:
            permission_dict[group_title]['urls'].append(permission['permission__url'])
            permission_dict[group_title]['actions'].append(permission['permission__action'])
        else:
            permission_dict[group_title]={
                'urls':[permission['permission__url']],
                'actions':[permission['permission__action']]
            }
        if permission['permission__action']==4:
            menu_list.append([(group_title),(permission['permission__url'])])
    print(menu_list)
    print(permission_dict)
    # 注册菜单列表
    request.session['menu_list'] = menu_list
    # 注册权限字典
    request.session['permission_dict'] = permission_dict
```

重写校验(rbac/service/rbac.py):

```python
# 检验权限
'''
        for permission in permission_list:
            permission = '^%s$' % permission
            ret = re.match(permission, url_path)
            if ret:
                return None
         return HttpResponse('没有权限')
'''
        for permission in permission_dict.values():
            urls = permission['urls']
            for url in urls:
                url = '^%s$' % url
                ret = re.match(url, url_path)
                if ret:
                    # 将动作加入request用于判断用户有没有这个操作权限
                    request.actions = permission['actions']
                    return None
        return HttpResponse('没有权限')
```

修改app01里的视图函数(app/views.py):

```python
# 新增一个类 用于判断用户是否有这个操作权限
class Permissions(object):
    #  action_list = [(1,'add'),(2,'delete'),(3,'update'),(4,'select')]
    def __init__(self,actions):
        self.actions=actions
    def add(self):
        return 1 in self.actions
    def delete(self):
        return 2 in self.actions
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
```

修改前端html 使用模版继承:

user.html:

```html
{% extends 'base.html' %}

{% block index %}
    <div class="row-rigth">
        <div class="table-list">
            <div class="panel panel-primary">
                <!-- Default panel contents -->
                <div class="panel-heading">用户列表</div>
                <div class="panel-body">
                    {% if permission.add %}
                    <a href="/user/add/"><div class="btn btn-primary">添加用户</div></a>
                    {% endif %}

                    <!-- Table -->
                    <table class="table table-bordered">

                        <tbody>
                        {% for user in get_list %}
                        <tr>
                            <th scope="row">{{ forloop.counter }}</th>
                            <td>{{ user.username }}</td>
                            <td>{{ user.password }}</td>
                            <td>
                                {% if permission.update %}
                                <a href="/user/edit/{{ user.pk }}"><div class="btn btn-warning">修改</div></a>

                                {% endif %}
                            {% if permission.delete %}
                            <a href="/user/delete/{{ user.pk }}"><div class="btn btn-danger">删除</div></a>
                            {% endif %}
                                  </td>
                        </tr>
                        {% endfor %}

                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

{% endblock %}
```

base.html:

```html
{% load get_menus_tag %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>后台管理</title>
    <!-- 最新版本的 Bootstrap 核心 CSS 文件 -->
    <script
  src="https://code.jquery.com/jquery-3.3.1.min.js"
  integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
  crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css"
          integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <style>
        .header {
            width: 100%;
            height: 50px;
            background-color: #101010;
        }

        .container {
            margin-top: 50px;
        }

        .row-left {
            width: 30%;
            height: 100%;
            position: fixed;
            top: 50px;
            bottom: 0;
            left: 0;
            right: 0;

            overflow: auto;
        }

        .row-rigth {
            width: 70%;
            height: auto;
            position: fixed;
            top: 50px;
            bottom: 0;
            right: 0;
            overflow: auto;

        }

        .menu {
            margin-top: 20px;
        }

        .table-list {
            margin-top: 20px;
            margin-left: 50px;
            margin-bottom: 50px;
            margin-right: 50px;
        }

        .menu-item {
            width: 70%;
            margin-left: 30px;
        }
    </style>

</head>
<body>
<div class="header">

</div>
<div class="container">
    <div class="row-left">
        <div class="menu">
            <div class="list-group">
                {% get_menu_list request as menus %}
                {% for menu in menus %}
                    <a href="{{ menu.1 }}" class="list-group-item menu-item">{{ menu.0 }}</a>
                {% endfor %}
            </div>
        </div>
    </div>
    {% block index %}
    {% endblock %}
    <div class="footer">
    </div>
    <script>
        $('.menu-item').each(function () {
           if (window.location.pathname===$(this).attr('href')){
              $(this).addClass('active')
           }
        })
    </script>
</div>
</body>
</html>
```

这里使用tag来做左侧菜单栏(rbac/templatatags/get_munus_tag.py):

```python
from django import template

register=template.Library()

@register.simple_tag
def get_menu_list(request):
    # 获取注册的菜单
    return request.session['menu_list']
```

效果图如下:

![](https://github.com/Tigercoll/my_picturelib/raw/master/rbac/3.gif)

代码已上传至[github](https://github.com/Tigercoll/rbac/tree/rbac-pro)


# 注册权限url列表到session

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
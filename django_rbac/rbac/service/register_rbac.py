# 注册权限url列表到session

def rbac_login(request,user):
    permission_dict = {}
    menu_list = []
    request.session['user_id'] = user.pk
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

    request.session['menu_list'] = menu_list
    request.session['permission_dict'] = permission_dict
# 注册权限url列表到session

def rbac_login(request,user):
    permission_list = []
    request.session['user_id'] = user.pk
    permissions = user.roles.all().values("permission__url").distinct()
    for permission in permissions:
        permission_list.append(permission['permission__url'])
    request.session['permission_list'] = permission_list
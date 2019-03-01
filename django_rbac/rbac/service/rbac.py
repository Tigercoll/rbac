# rbac 中间件

import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import  HttpResponse,redirect

class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url_path = request.path_info

        # 白名单 white_list 要加斜线
        white_list = ['/login/','/.*/static/.*','/admin/.*']

        permission_dict = request.session.get('permission_dict',{})

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
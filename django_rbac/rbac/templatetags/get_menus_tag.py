from django import template

register=template.Library()

@register.simple_tag
def get_menu_list(request):
    # 获取注册的菜单
    return request.session['menu_list']
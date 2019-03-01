from django import template

register=template.Library()

@register.simple_tag
def get_menu_list(request):
    return request.session['menu_list']
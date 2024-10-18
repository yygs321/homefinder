from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """문자열을 주어진 구분자로 나누는 필터"""
    return value.split(arg)
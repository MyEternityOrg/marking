from django import template

register = template.Library()


@register.simple_tag(name='user_login_name')
def get_login_full_name(user):
    if user.first_name and user.last_name:
        return ' '.join([user.first_name, user.last_name])
    return user.username

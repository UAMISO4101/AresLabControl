from django import template

register = template.Library()


@register.filter(name = 'addcss')
def addcss(field, css):
    return field.as_widget(attrs = {"class": css, "placeholder": field.name.title()})

import types
from copy import copy

from django.contrib.humanize.templatetags.humanize import intcomma
from django.template import Library

register = Library()


@register.filter(name = 'addcss')
def addcss(field, css):
    return field.as_widget(attrs = {"class": css, "placeholder": field.name.title()})


@register.filter(name = 'attr')
def set_attr(field, attr):
    def process(widget, attrs, attribute, value):
        attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


@register.filter(name = 'currency')
def currency(dollars):
    dollars = round(float(dollars), 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])


def _process_field_attributes(field, attr, process):
    # split attribute name and value from 'attr:value' string
    params = attr.split(':', 1)
    attribute = params[0]
    value = params[1] if len(params) == 2 else ''
    field = copy(field)

    # decorate field.as_widget method with updated attributes
    old_as_widget = field.as_widget

    def as_widget(self, widget = None, attrs = None, only_initial = False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html

    field.as_widget = types.MethodType(as_widget, field)
    return field


@register.filter(name = 'lookup')
def lookup(d, key):
    return d.get(key, None)

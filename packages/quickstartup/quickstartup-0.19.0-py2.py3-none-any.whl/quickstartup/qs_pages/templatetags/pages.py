from django import template

from quickstartup.qs_pages.urlresolver import page_reverse

register = template.Library()


@register.simple_tag
def page_url(slug):
    return page_reverse(slug)

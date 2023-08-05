import logging

from django import template

register = template.Library()
logger = logging.getLogger(__name__)


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return context["request"].site.root_page


@register.inclusion_tag("components/menu/top_menu.html")
def top_menu(parent, first_level=False):
    menuitems = parent.get_children().live().in_menu()
    items = []
    for menuitem in menuitems:
        real_page = menuitem.specific
        real_page.show_dropdown = (
            first_level and len(real_page.get_children().live().in_menu()) > 0
        )
        items.append(real_page)
    return {"menuitems": items}

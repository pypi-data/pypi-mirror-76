from coldcms.site_settings.models import Footer
from django import template

register = template.Library()


@register.simple_tag
def get_footer_columns():
    try:
        footer = Footer.objects.first()
        return footer.columns.all()
    except Exception:
        return []

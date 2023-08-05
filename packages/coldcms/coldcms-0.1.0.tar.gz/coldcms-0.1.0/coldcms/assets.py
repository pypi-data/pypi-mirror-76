import os

from django.conf import settings
from django_assets import Bundle, register

css_all_output = "css/app.css"
ORIGINAL_CSS_PATH = os.path.join(settings.STATIC_ROOT, f"{css_all_output}.original.css")


def _replace_original_css(_in, out, **kw):
    css_content = _in.read()
    out.write(css_content)
    os.makedirs(os.path.dirname(ORIGINAL_CSS_PATH), exist_ok=True)
    with open(ORIGINAL_CSS_PATH, "w") as f:
        f.write(css_content)


scss = Bundle("scss/app.scss", filters="scss", output="css/app.scss")

css_all = Bundle(scss, filters="cssrewrite", output=css_all_output)

css_all = Bundle(css_all, filters=(_replace_original_css,), output=css_all_output)

register("css_all", css_all)

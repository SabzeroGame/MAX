from django import template

register = template.Library()


@register.filter
def short_text(value: str, length: int = 120):
    value = value or ""
    return value if len(value) <= length else f"{value[:length].rstrip()}..."
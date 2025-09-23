from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def insert_break(value, num):
    """
    Inserts a <wbr> tag after a given number of characters.
        value: Input value
        num: Number of characters between optional breaks
    """
    step = int(num)
    if not isinstance(value, str):
        value = str(value)
    parts = [value[i : i + step] for i in range(0, len(value), step)]
    return mark_safe("<wbr>".join(parts))

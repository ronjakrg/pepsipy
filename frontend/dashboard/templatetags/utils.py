from django import template

register = template.Library()


@register.filter
def insert_break(value, arg):
    """
    Inserts a <br>-Tag after a given number of characters.
        value: Input value
        arg: Number of characters between breaks
    """
    number = int(arg)
    if not isinstance(value, str):
        value = str(value)
    return "<br>".join(value[i : i + number] for i in range(0, len(value), number))

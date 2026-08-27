from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def email_input(required=True): #<label for="email">{{ x.text }}</label>
    if required:
        return mark_safe('<input type="email" id="email" name="email" placeholder="you@example.com" required>')
    else:
        return mark_safe('<input type="email" id="email" name="email" placeholder="you@example.com">')
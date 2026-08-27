from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def email_input(name, required=True): #<label for="email">{{ x.text }}</label>
    if required:
        return mark_safe(f'<input type="email" id="{name}" name="{name}" placeholder="you@example.com" required>')
    else:
        return mark_safe(f'<input type="email" id="{name}" name="{name}" placeholder="you@example.com">')

@register.simple_tag
def short_text(name, required=True, placeholder='Type your answer'):
    if required:
        return mark_safe(f'<input type="text" id="{name}" name="{name}" placeholder="{placeholder}" required>')
    else:
        return mark_safe(f'<input type="text" id="{name}" name="{name}" placeholder="{placeholder}">')

@register.simple_tag
def long_text(name, rows=10, cols=60, required=False, placeholder='Type your answer'):
    if required:
        return mark_safe(f'<textarea id="{name}" name="{name}" placeholder="{placeholder}" rows="{rows}" cols="{cols}" required></textarea>')
    else:
        return mark_safe(f'<textarea id="{name}" name="{name}" placeholder="{placeholder}" rows="{rows}" cols="{cols}"></textarea>')

@register.simple_tag
def rating_1_5(name, required=True):
    if required:
        html = f'''
        <input type="radio" id="r5" name="{name}" value="5" required>
        <label for="r5">★★★★★</label><br>
        <input type="radio" id="r4" name="{name}" value="4" required>
        <label for="r4">★★★★☆</label><br>
        <input type="radio" id="r3" name="{name}" value="3" required>
        <label for="r3">★★★☆☆</label><br>
        <input type="radio" id="r2" name="{name}" value="2" required>
        <label for="r2">★★☆☆☆</label><br>
        <input type="radio" id="r1" name="{name}" value="1" required>
        <label for="r1">★☆☆☆☆</label>'''
    else:
        html = f'''
        <input type="radio" id="r5" name="{name}" value="5">
        <label for="r5">★★★★★</label><br>
        <input type="radio" id="r4" name="{name}" value="4">
        <label for="r4">★★★★☆</label><br>
        <input type="radio" id="r3" name="{name}" value="3">
        <label for="r3">★★★☆☆</label><br>
        <input type="radio" id="r2" name="{name}" value="2">
        <label for="r2">★★☆☆☆</label><br>
        <input type="radio" id="r1" name="{name}" value="1">
        <label for="r1">★☆☆☆☆</label>'''

    return mark_safe(html)
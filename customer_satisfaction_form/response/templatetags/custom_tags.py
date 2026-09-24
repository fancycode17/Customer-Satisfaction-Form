from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('widgets/email_input.html') #sends results to email_input.html
def email_input(q, submitted_data, placeholder='you@example.com'):
    return { #dictionary containing Question object, preset value and placeholder
        'q':q,
        'value': submitted_data.get(f'question_{q.id}', ''),#value = submitted data for that question if applicable, else ''
        'placeholder': placeholder,
    }

@register.inclusion_tag('widgets/short_text.html')
def short_text(q, submitted_data, placeholder='Type your answer'):
    return {
        'q': q,
        'value': submitted_data.get(f'question_{q.id}', ''),
        'placeholder': placeholder
    }

@register.inclusion_tag('widgets/long_text.html')
def long_text(q, submitted_data, rows=10, cols=60, placeholder='Type your answer'):
    return {
        'q': q,
        'value': submitted_data.get(f'question_{q.id}', ''),
        'rows':rows,
        'cols':cols,
        'placeholder':placeholder,
    }

@register.inclusion_tag('widgets/rating_1_5.html')
def rating_1_5(q, submitted_data):
    return {
        'q':q,
        'checked': submitted_data.get(f'question_{q.id}', ''),
    }

@register.inclusion_tag('widgets/rating_1_10.html')
def rating_1_10(q, submitted_data):
    return {
        'q':q,
        'value': submitted_data.get(f'question.{q.id}', ''),
    }

@register.inclusion_tag('widgets/multi_select.html')
def multi_select(q, submitted_data):
    print(submitted_data.get(f'other_detail_{q.id}', '')=='')
    return {
        'q': q,
        'options': q.options.filter(is_active=True).order_by("display_order"),
        'checked': submitted_data.get(f'question.{q.id}', ''),
        'other_detail': submitted_data.get(f'other_detail_{q.id}', ''),
    }

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
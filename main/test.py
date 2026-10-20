import os
import django

# 1. Point to your Django project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customer_satisfaction_form.settings")

# 2. Setup and initialize Django
django.setup()

# 3. Now you can safely import your apps and models
from app.models import Question
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def invalid_multi_select(q, post_data, errors):
    #returns flat list of the labels of options tied to the question
    valid_selections = list(q.options.values_list('label', flat=True))
    invalid_selections = []
    #post_data.get() only returns a single value so getlist() is used in case multiple options have been selected
    for selection in post_data.getlist(f'question_{q.id}'):
        if selection not in valid_selections:
            invalid_selections.append(selection)

        if selection == 'Other':
            other = post_data.get(f'other_detail_{q.id}', '')
            if not other.strip():
                errors.setdefault(f'question_{q.id}', []).append('Please elaborate')
    return invalid_selections, errors

def check_errors(post_data):
    '''Example output: 
    {'question_1': ['Answer required.'], 'question_2': [], 
    'question_3': [], 'question_4': ['Please elaborate', 'The following selections are invalid: Psh notifications'], 
    'question_5': [], 'question_6': [], 'question_7': []}'''

    errors = {}
    questions = Question.objects.filter(is_active=True)

    for q in questions:
        errors[f'question_{q.id}'] = []
        #get value of response for the question ('' if not included in POST request)
        if q.type =='multi-select':
            selections = post_data.getlist(f'question_{q.id}')
            if q.is_required and not selections:
                errors[f'question_{q.id}'].append('Answer required.')
                continue

            invalid, errors = invalid_multi_select(q, post_data, errors)
            if invalid:
                errors[f'question_{q.id}'].append(
                    f'The following selections are invalid: {', '.join(invalid)}'
                    )
                
        else:
            value = post_data.get(f'question_{q.id}', '')

            if q.is_required and not value.strip():
                errors[f'question_{q.id}'].append('Answer required.')
                continue

            if q.type == 'rating_1-5':
                if not value.isdigit():
                    errors[f'question_{q.id}'].append('Answer must be an integer')
                elif not (1 <= int(value) <= 5):
                    errors[f'question_{q.id}'].append('Answer must be between 1 and 5')
            elif q.type == 'rating_1-10':
                if not value.isdigit():
                    errors[f'question_{q.id}'].append('Answer must be an integer')
                elif not 1 <= int(value) <= 10:
                    errors[f'question_{q.id}'].append('Answer must be between 1 and 10')
            elif q.type == 'email' and not valid_email(value):
                errors[f'question_{q.id}'].append('Invalid email format')            

    return errors

def no_errors(errors):
    no_errors = True
    for item in errors.values():
        if item:
            no_errors = False
    
    return no_errors
from django.http import QueryDict

post_data = QueryDict('', mutable=True)
post_data.setlist('question_1', [''])
post_data.setlist('question_2', ['3'])
post_data.setlist('question_3', [''])
post_data.setlist('question_5', ['1'])
post_data.setlist('question_6', ['jibran'])
post_data.setlist('question_7', ['jibran@example.com'])

# For multi-select:
post_data.setlist('question_4', ['Push notifications', 'Video calling/Virtual inspection'])

errors = check_errors(post_data)
print(errors)
print(no_errors(errors))

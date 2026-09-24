from .models import Question
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
    submitted_data = {}
    questions = Question.objects.filter(is_active=True)

    for q in questions:
        key = f'question_{q.id}'
        errors[key] = []
        #get value of response for the question ('' if not included in POST request)
        if q.type =='multi-select':
            selections = post_data.getlist(key)
            other_detail = post_data.get(f'other_detail_{q.id}','')
            if other_detail:
                submitted_data[f'other_detail_{q.id}'] = other_detail
                #selections.append(f'Other: {other_detail}')
            submitted_data[key] = selections
        
            if q.is_required and not selections:
                errors[key].append('Answer required.')
                continue

            invalid, errors = invalid_multi_select(q, post_data, errors)
            if invalid:
                errors[key].append(
                    f"The following selections are invalid: {', '.join(invalid)}"
                    )
                
        else:
            value = post_data.get(key, '')
            submitted_data[key] = value

            if q.is_required and not value.strip():
                errors[key].append('Answer required.')
                continue

            if q.type == 'rating_1-5':
                if value == '':
                    continue
                else:
                    if not value.isdigit():
                        errors[key].append('Answer must be an integer')
                    elif not (1 <= int(value) <= 5):
                        errors[key].append('Answer must be between 1 and 5')
            elif q.type == 'rating_1-10':
                if not value.isdigit():
                    errors[key].append('Answer must be an integer')
                elif not 1 <= int(value) <= 10:
                    errors[key].append('Answer must be between 1 and 10')
            elif q.type == 'email' and not valid_email(value):
                errors[key].append('Invalid email format')            

    return errors, submitted_data

def get_client(email):
    domain = email.split('@')[1]
    client = domain.split('.')[0]
    return client

def get_email(keys):
    questions = Question.objects.filter(is_active=True)
    for key in keys:
        if key.startswith('question_'):
            id = key.split('_')[1]
            q = questions.filter(id=id)[0]
            if q.type == 'email':
                return key

def no_errors(errors):
    no_errors = True
    for item in errors.values():
        if item:
            no_errors = False
    
    return no_errors
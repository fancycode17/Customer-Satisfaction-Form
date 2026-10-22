from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Question, Submission, Answer
from .helper import get_client, get_email, get_name, check_errors, no_errors
from datetime import datetime

def main(request):
    questions = Question.objects.filter(is_active=True).order_by('display_order')
    template = loader.get_template('main.html')
    errors = {}
    submitted_data = {}

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data.pop('csrfmiddlewaretoken', None)
        errors, submitted_data = check_errors(post_data)
        email = post_data.get(get_email(post_data.keys()),"N/A")
        if no_errors(errors):
            submission = Submission.objects.create(
                submitted_at=datetime.now(),
                name=post_data.get(get_name(post_data.keys()),"N/A"),
                email= email,
                client= get_client(email)
            )

            for q in questions:
                values = request.POST.getlist(f'question_{q.id}')
                if values:
                    if q.type == 'MSELECT':
                        other_detail = request.POST.getlist(f'other_detail_{q.id}')[0]
                        selected = []
                        for value in values:
                            if value == 'Other':
                                value += f': {other_detail}'
                            selected.append(value)

                        Answer.objects.create(
                            submission=submission,
                            question=q,
                            value=', '.join(selected),
                            display_order=q.display_order
                        )
                    else:
                        Answer.objects.create(
                            submission=submission,
                            question=q,
                            value=', '.join(values),
                            display_order=q.display_order
                        )

            return redirect('success')
        else:
            print(errors)

    context = {
                'questions': questions,
                'errors': errors,
                'submitted_data': submitted_data
            }
    
    return HttpResponse(template.render(context, request))

def success(request):
    template = loader.get_template('template.html')
    return HttpResponse(template.render())
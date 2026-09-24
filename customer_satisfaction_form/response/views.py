from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Response, Question, Submission, Answer
from .helper import get_client, get_email, check_errors, no_errors
from datetime import datetime

def responses(request):
    myresponses = Response.objects.all().order_by('-joined_date').values()
    template = loader.get_template('all_responses.html')
    context = {
        'myresponses': myresponses,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myresponse = Response.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myresponse': myresponse,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    questions = Question.objects.filter(is_active=True).order_by('display_order')
    template = loader.get_template('main.html')
    errors = {}
    submitted_data = {}

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data.pop('csrfmiddlewaretoken', None)
        errors, submitted_data = check_errors(post_data)
                    
        print(post_data)
        if no_errors(errors):
            submission = Submission.objects.create(
                submitted_at=datetime.now(),
                name=post_data.get("name",""),
                email=post_data.get(get_email(post_data.keys()),""),
                client='Example'
            )

            for q in questions:
                values = request.POST.getlist(f'question_{q.id}')
                if values:
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
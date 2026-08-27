from django.http import HttpResponse
from django.template import loader
from .models import Response, Question

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
    questions = Question.objects.filter(is_active=True).order_by('display_order').values()
    template = loader.get_template('main.html')
    context = {
            'questions': questions,
        }
    return HttpResponse(template.render(context, request))

def testing(request):
    myresponses = Response.objects.all().order_by('-joined_date').values()
    template = loader.get_template('template.html')
    context = {
        'myresponses': myresponses,
    }
    return HttpResponse(template.render(context, request))
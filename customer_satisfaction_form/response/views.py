from django.http import HttpResponse
from django.template import loader
from .models import Response

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
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def testing(request):
    myresponses = Response.objects.all().order_by('-joined_date').values()
    template = loader.get_template('template.html')
    context = {
        'myresponses': myresponses,
    }
    return HttpResponse(template.render(context, request))
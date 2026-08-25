from django.contrib import admin
from .models import Response

# Register your models here.

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'joined_date')

admin.site.register(Response, ResponseAdmin)
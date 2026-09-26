from django.contrib import admin
from .models import Submission, Answer

# Register your models here.

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submitted_at', 'name', 'email', 'client')
    search_fields = ('submitted_at', 'name', 'email', 'client')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'question_id', 'value', 'display_order')

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Answer, AnswerAdmin)
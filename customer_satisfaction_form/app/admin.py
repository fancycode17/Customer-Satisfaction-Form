from django.contrib import admin
from .models import Submission, Answer, Question, Option

# Register your models here.

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submitted_at', 'name', 'email', 'client')
    search_fields = ('submitted_at', 'name', 'email', 'client')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'question_id', 'value', 'display_order')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'help_text', 'type', 'version', 'is_active', 'is_required', 'display_order')

class OptionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'label', 'is_active', 'display_order')

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
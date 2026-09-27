from django.contrib import admin
from .models import Submission, Answer, Question, Option

# Register your models here.
class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 0
    #readonly_fields = ('text','type', 'version', 'is_active',)
    readonly_fields = ('question_text','question_type','question_version','question_is_active')

    def question_text(self, obj):
        return obj.question.text

    def question_type(self, obj):
            return obj.question.type

    def question_version(self, obj):
                return obj.question.version

    def question_is_active(self, obj):
                return obj.question.is_active
    
    question_text.short_description = "Question"

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submitted_at', 'name', 'email', 'client',)
    search_fields = ('name', 'email', 'client',)
    list_filter = ('submitted_at',)
    inlines = [AnswerInLine]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'help_text', 'type', 'version', 'is_active', 'is_required', 'display_order')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'label', 'is_active', 'display_order')
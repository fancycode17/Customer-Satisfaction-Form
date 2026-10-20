import csv
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.http import HttpResponse
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
    actions = ['export_submissions_csv', 'export_answers_csv']

    def export_submissions_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=submissions.csv'

        writer = csv.writer(response)

        #Header row
        writer.writerow([
            'submitted_at',
            'name',
            'email',
            'client',
        ])

        #Data rows
        for submission in queryset:
            writer.writerow([
                    submission.submitted_at,
                    submission.name,
                    submission.email,
                    submission.client,
            ])

        return response
    
    export_submissions_csv.short_description = 'Export brief submission data as CSV'
    
    def export_answers_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=submission_data.csv'

        writer = csv.writer(response)

        #Header row
        writer.writerow([
            'submission',
            'submitted_at',
            'name',
            'email',
            'client',
            'question_text',
            'question_type',
            'question_version',
            'question_is_active',
            'answer_value',
        ])

        submission_number = 0
        #Data rows
        for submission in queryset:
            submission_number += 1
            answers = Answer.objects.filter(submission=submission)

            for ans in answers:
                q = ans.question
                writer.writerow([
                      submission_number,
                      submission.submitted_at,
                      submission.name,
                      submission.email,
                      submission.client,
                      q.text,
                      q.type,
                      q.version,
                      q.is_active,
                      ans.value
                ])

        return response
    
    export_answers_csv.short_description = 'Export answers for selected submissions (with question data) as CSV'

class OptionInLine(admin.TabularInline):
    model = Option
    extra = 1 #empty row for adding new options
    can_delete = False

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'help_text', 'type', 'version', 'is_active', 'is_required', 'display_order')
    search_fields = ('text', 'type', 'version', 'is_active', 'is_required')
    inlines = [OptionInLine]

    def clean(self):
        active_count = self.options.filter(is_active=True).count()
        if active_count < 2:
              raise ValidationError('Each question must have at least two active options.')

    def save(self, *args, **kwargs):
        #validate before saving
        self.clean()
        super().save(*args, **kwargs)
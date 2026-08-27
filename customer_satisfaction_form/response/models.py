from django.db import models

class Response(models.Model):
    firstname = models.CharField(max_length=225)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Question(models.Model): #uses Django ORM to create a database table. each variable is a column
    text = models.CharField(max_length=255)
    help_text = models.CharField()
    type = models.CharField(max_length=15)
    version = models.SmallIntegerField()
    active = models.BooleanField()
    display_order = models.SmallIntegerField()

class Option(models.Model):
    question = models.ForeignKey( #links Option to Question so calls such as Option.question.id can be made
        Question, on_delete=models.PROTECT, related_name='options'
        )
    label = models.CharField(max_length=100)
    display_order = models.SmallIntegerField()

class Submission(models.Model):
    submitted_at = models.DateTimeField()
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    client = models.CharField(max_length=255)

class Answer(models.Model):
    #will access submission id
    submission = models.ForeignKey(
        Submission, on_delete=models.PROTECT, related_name='answers'
    )
    #will access question id, text, type, and version
    question = models.ForeignKey(
        Question, on_delete=models.PROTECT, related_name='answers'
    )
    value = models.CharField()
    display_order = models.SmallIntegerField()
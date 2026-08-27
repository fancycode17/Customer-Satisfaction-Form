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
    help_text = models.CharField(blank=True)
    type = models.CharField(max_length=15)
    version = models.SmallIntegerField()
    is_active = models.BooleanField(db_default=True)
    is_required = models.BooleanField()
    display_order = models.SmallIntegerField(blank=True)

    def save(self, *args, **kwargs): #overrides default save() function
        # Only auto-assign if display_order wasn't set manually
        if self.display_order is None: #if display_order hasn't been manually set:
            #find the maximum value of display_order in the table
            last_order = Question.objects.aggregate(models.Max("display_order"))["display_order__max"]
            self.display_order = (last_order or 0) + 1 #add one to the current max display_order (or 0 if it is the first row)
        super().save(*args, **kwargs) #call the default save() function to apply changes

class Option(models.Model):
    question = models.ForeignKey( #links Option to Question so calls such as Option.question.id can be made
        Question, on_delete=models.PROTECT, related_name='options'
        )
    label = models.CharField(max_length=100)
    display_order = models.SmallIntegerField(blank=True)
    is_active = models.BooleanField(db_default=True)

    def save(self, *args, **kwargs): #overrides default save() function
        # Only auto-assign if display_order wasn't set manually
        if self.display_order is None: #if display_order hasn't been manually set:
            #find the maximum value of display_order in the table
            last_order = Question.objects.aggregate(models.Max("display_order"))["display_order__max"]
            self.display_order = (last_order or 0) + 1 #add one to the current max display_order (or 0 if it is the first row)
        super().save(*args, **kwargs) #call the default save() function to apply changes

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
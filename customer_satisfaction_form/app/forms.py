from django import forms
from django.core.validators import MinLengthValidator

class InputForm(forms.Form):
    first_name = forms.CharField(max_length=200,
                                 validators=[MinLengthValidator(5)]
                                 )
    last_name = forms.CharField(max_length=200)
    
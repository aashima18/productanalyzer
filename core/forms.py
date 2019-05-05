from django import forms
from .models import Feedback
from django.forms import ModelForm


class SearchForm(forms.Form):

    query = forms.CharField()

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'


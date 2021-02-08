from django import forms
from .models import SeoProject


class SuggestionForm(forms.Form):
    project = forms.ModelChoiceField(queryset=SeoProject.objects.all())


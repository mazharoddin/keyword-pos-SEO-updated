from django import forms
from .models import Keyword, City


class SearchForm(forms.Form):
    site = forms.ModelChoiceField(queryset=Keyword.objects.all())
    cities = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=City.objects.all(), required=False
    )


class MapSearchForm(forms.Form):
    site = forms.ModelChoiceField(queryset=Keyword.objects.all())


class ReportForm(forms.Form):
    site = forms.ModelChoiceField(queryset=Keyword.objects.all())
    date = forms.DateField(
        localize=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )
    is_map = forms.BooleanField(required=False)


class GraphReportForm(forms.Form):
    INTERVAL_CHOICES = (
        ("1", "One Month"),
        ("3", "Three Month"),
        ("6", "Six Month"),
        ("12", "One Year"),
    )
    site = forms.ModelChoiceField(queryset=Keyword.objects.all())
    interval = forms.ChoiceField(choices=INTERVAL_CHOICES)


class UploadFileForm(forms.Form):
    file = forms.FileField()


class KeywordToUrlFrom(forms.Form):
    keyword = forms.CharField(max_length=100)
    url_text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 60}),
        required=False,
        label="URL Text",
    )

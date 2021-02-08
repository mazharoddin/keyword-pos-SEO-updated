from django import forms
from .models import JobDetail


class JobDetailForm(forms.ModelForm):
    class Meta:
        model = JobDetail
        fields = ["title", "location", "job_url", "summary", "confirm"]
        # readonly_fields = ("is_new",)

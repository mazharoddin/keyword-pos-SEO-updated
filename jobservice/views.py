from django.shortcuts import render
from django.views.generic import ListView
from .forms import JobDetailForm
from .models import JobDetail


class JobListView(ListView):
    model = JobDetail
    form = JobDetailForm
    template_name = "jobservice/jobdetails.html"


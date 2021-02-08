from django.contrib import admin
from django.contrib.auth import get_user_model
from keyservice.admin import admin_site
from .models import SeoProject, KeywordSuggestion


admin_site.register(SeoProject)
admin_site.register(KeywordSuggestion)


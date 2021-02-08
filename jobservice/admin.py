from django.contrib import admin
from keyservice.admin import admin_site
from .models import KeywordToCity, JobKeyword, City, JobDetail


admin_site.register(JobKeyword)
admin_site.register(KeywordToCity)
admin_site.register(City)
admin_site.register(JobDetail)


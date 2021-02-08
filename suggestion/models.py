from django.db import models


class SeoProject(models.Model):
    project_name = models.CharField(max_length=150)
    keywords = models.TextField()
    url = models.CharField(max_length=150, blank=True, null=True)
    cities = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.project_name


class KeywordSuggestion(models.Model):
    keyword = models.CharField(max_length=150)
    suggestion = models.TextField()
    project = models.ForeignKey(SeoProject, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.project, self.keyword)

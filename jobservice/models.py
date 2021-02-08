from django.db import models
from django.utils.timezone import datetime


class JobKeyword(models.Model):
    keyword = models.TextField()

    def __str__(self):
        return self.keyword


class City(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "%s, %s" % (self.city, self.state)


class KeywordToCity(models.Model):
    keyword = models.ForeignKey(JobKeyword, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.keyword} {self.city}"


class JobDetail(models.Model):
    title = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    job_url = models.URLField()
    summary = models.TextField()
    confirm = models.BooleanField()
    date_added = models.DateField(auto_now_add=True)

    @property
    def is_new(self):
        today = datetime.now().date()
        latest_qs = JobDetail.objects.filter(date_added=today)
        if latest_qs.exists():
            return True
        return False


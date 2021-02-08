import datetime
from django.db import models
# from django.contrib.auth import get_user_model


class Keyword(models.Model):
    title = models.CharField(max_length=70)
    urls = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default="")
    it_has_map = models.BooleanField(default=False)
    priority_keyword = models.TextField(default="")
    main_keyword = models.TextField()
    secondary_keyword = models.TextField()

    def __str__(self):
        return "%s" % self.title


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % self.name


class Position(models.Model):
    seq_no = models.IntegerField(default=0)
    position = models.IntegerField()
    url = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    date = models.DateField(default=datetime.date.today)
    verified = models.BooleanField(default=False)
    keyword_id = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s - %s -  %s" % (
            self.date,
            self.url,
            self.key,
            self.city,
            self.position,
        )


class MapPosition(models.Model):
    seq_no = models.IntegerField(default=0)
    position = models.IntegerField()
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    date = models.DateField(default=datetime.date.today)
    verified = models.BooleanField(default=False)
    # keyword_id = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s - %s -  %s" % (
            self.date,
            self.name,
            self.key,
            self.city,
            self.position,
        )


class KeywordCityRel(models.Model):
    keyword_id = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.keyword_id, self.city_id)

from datetime import date
from django.contrib import admin
from django.http.request import HttpRequest
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.contrib.admin import widgets
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ngettext
from urllib.parse import quote_plus
from django.utils.html import format_html
from .models import Keyword, City, Position, MapPosition, KeywordCityRel

from django.contrib.admin import AdminSite, ModelAdmin, DateFieldListFilter, SimpleListFilter


class MyAdminSite(AdminSite):
    site_header = "Desss SEO Tool Admin"
    site_title = "Desss SEO Tool Admin Portal"
    index_title = "Welcome to Desss SEO Tool Portal"


admin_site = MyAdminSite(name="Desss Admin")


class LastMonthFilter(SimpleListFilter):
    title = "Last Month"
    parameter_name = "last_month"

    def lookups(self, request, model_admin):
        return (("last_month", "Last Month"),)

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        print(self.value())
        if self.value():
            today = datetime.today()
            last_month = today - relativedelta(months=1)
            return queryset.filter(
                date__year=str(last_month.year), date__month=str(last_month.month),
            )
        else:
            return queryset


class DateChangeForm(ActionForm):
    date = forms.DateField(required=False)
    verified = forms.BooleanField(required=False)


class PositionAdmin(ModelAdmin):
    list_display = ("date", "url", "city", "verified", "position", "get_previous_position")
    list_filter = ("keyword_id__urls", "date", LastMonthFilter, "city", "verified")
    search_fields = ("url", "date", "city")
    actions = ["change_date"]
    action_form = DateChangeForm

    def get_previous_position(self, obj):
        # print(obj.date.month)
        queryset = Position.objects.filter(
            url=obj.url, city=obj.city, key=obj.key, date__month__lt=obj.date.month
        )

        return [qs.position for qs in queryset]

    get_previous_position.short_description = "Previous Position"

    def change_date(self, request, queryset):
        # print(".....")
        updated = 0
        date = request.POST.get("date", None)
        verified = request.POST.get("verified", None)
        if date:
            updated = queryset.update(date=date)
        if verified:
            updated = queryset.update(verified=True)
        self.message_user(
            request,
            ngettext(
                "%d records was successfully Updated.",
                "%d records was successfully Updated.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    change_date.short_description = "Apply action on selected"
    change_date.allowed_permissions = ("change",)

    # def make_verified(self, request, queryset):
    #     print(".........")
    #     update = queryset.update(verified=True)

    # make_verified.short_description = "Change verified True"
    # make_verified.allowed_permissions = ("change",)

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True


class MapPositionAdmin(ModelAdmin):
    list_display = ("date", "name",'key', "city", "verified", "position", "get_previous_position","show_google")
    list_filter = ("name", "date", LastMonthFilter, "city", "verified")
    search_fields = ("name", "date", "city")
    actions = ["change_date"]
    action_form = DateChangeForm

    def show_google(self, obj):
        query=obj.key+" "+obj.city
        quoted_string=quote_plus(query)
        url = "http://www.google.com/search?gl=us&q=%s&num=20&hl=en&start=0" % (quoted_string)
        return format_html('<a href="%s" target="_blank">%s</a>' % (url,obj.key))
    show_google.allow_tags = True


    def get_previous_position(self, obj):
        # print(obj.date.month)
        queryset = MapPosition.objects.filter(
            name=obj.name, city=obj.city, key=obj.key, date__month__lt=obj.date.month
        )

        return [qs.position for qs in queryset]

    get_previous_position.short_description = "Previous Position"

    def change_date(self, request, queryset):
        print(".....")
        updated = 0
        date = request.POST.get("date", None)
        verified = request.POST.get("verified", None)
        if date:
            updated = queryset.update(date=date)
        if verified:
            updated = queryset.update(verified=True)
        self.message_user(
            request,
            ngettext(
                "%d records was successfully Updated.",
                "%d records was successfully Updated.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    change_date.short_description = "Apply action on selected"
    change_date.allowed_permissions = ("change",)

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True


User = get_user_model()


admin_site.register(Keyword)
admin_site.register(City)
admin_site.register(Position, PositionAdmin)
admin_site.register(MapPosition, MapPositionAdmin)
admin_site.register(KeywordCityRel)

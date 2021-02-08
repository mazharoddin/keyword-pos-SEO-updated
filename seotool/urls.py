from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from keyservice.admin import admin_site
from keyservice.views import (
    index,
    get_position,
    get_report,
    upload_file,
    upload_file_map,
    delete_positions,
    get_cities,
    get_last_record,
    get_map_position,
    get_graph_report,
    get_urls_from_keyword,
    test_from,
)
from keyservice.api.views import GoogleKeywordIdea, signin, user_info, PositionListApiView
from suggestion.views import suggestion_service
from suggestion.api.views import BarcodeApiView
from jobservice.views import JobListView

urlpatterns = [
    # Admin urls
    path("admin/", admin_site.urls),
    # main urls
    path("", index, name="index"),
    path("search/", get_position, name="search"),
    path("map-search/", get_map_position, name="map-search"),
    path("report/", get_report, name="report"),
    path("graph-report/", get_graph_report, name="graph-report"),
    path("upload/", upload_file, name="upload"),
    path("map_upload",upload_file_map, name="map_upload"),
    path("delete/", delete_positions, name="delete"),
    path("suggestion/", suggestion_service, name="key-suggestion"),
    path("key-to-url/", get_urls_from_keyword, name="keyword-to-url"),
    path("test/", test_from, name="test-from"),
    path("job-list/", JobListView.as_view(), name="job-list"),
    path(
        "loading/", TemplateView.as_view(template_name="keyservice/loading.html"), name="loading",
    ),
    # Sub urls
    path("get-cities", get_cities, name="get-cities"),
    path("get-last-record", get_last_record, name="last-record"),
    # Api urls
    path("barcode/", BarcodeApiView.as_view(), name="barcode"),
    path("keyword-idea", GoogleKeywordIdea.as_view(), name="google-keyword-idea"),
    path("signin", signin, name="signin"),
    path("token-info", user_info, name="token-info"),
    path("api/", include("keyservice.api.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from .views import PositionListApiView, MapPositionListApiView


urlpatterns = [
    path("get-positions/", PositionListApiView.as_view(), name="get-positions"),
    path("get-map-positions/", MapPositionListApiView.as_view(), name="get-map-positions"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.overview, name="overview"),
    path("download_data",views.download_data, name="download_data")
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.overview, name="overview"),
    path("download_data", views.download_data, name="download_data"),
    path("download_plots", views.download_plots, name="download_plots"),
    path(
        "fill_metadata_options",
        views.fill_metadata_options,
        name="fill_metadata_options",
    ),
]

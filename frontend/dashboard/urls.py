from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("download_data", views.download_data, name="download_data"),
    path("download_plots", views.download_plots, name="download_plots"),
    path(
        "save_colors_from_modal",
        views.save_colors_from_modal,
        name="save_colors_from_modal",
    ),
    path("privacy", views.privacy, name="privacy"),
    path("imprint", views.imprint, name="imprint"),
]

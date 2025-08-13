from django.urls import path

from .views import MeView
from .views_labels import LabelsView

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("labels/", LabelsView.as_view(), name="labels"),
]

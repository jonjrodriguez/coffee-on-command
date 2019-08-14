from django.urls import path

from .views import IndexView, ResponseView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("response", ResponseView.as_view(), name="response"),
]


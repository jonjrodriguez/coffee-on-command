from django.urls import path

from .views import IndexView, ResponseView, EventsView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("response", ResponseView.as_view(), name="response"),
    path("event", EventsView.as_view(), name="event"),
]


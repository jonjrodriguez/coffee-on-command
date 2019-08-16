from django.urls import path

from .views import IndexView, CommandView, EventsView, ResponseView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("command", CommandView.as_view(), name="command"),
    path("response", ResponseView.as_view(), name="response"),
    path("event", EventsView.as_view(), name="event"),
]


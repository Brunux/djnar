from django.urls import path

from . import views


urlpatterns = [
    path('', views.EventsView.as_view(), name='index'),
    path('event', views.EventView.as_view(), name='event'),
]

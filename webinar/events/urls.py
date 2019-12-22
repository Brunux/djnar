from django.urls import path

from . import views


urlpatterns = [
    path('events/', views.EventsView.as_view(), name='events'),
]

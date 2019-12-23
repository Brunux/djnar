from django.urls import path

from . import views


urlpatterns = [
    path('', views.ContactsView.as_view(), name='index'),
]

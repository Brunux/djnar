from django.urls import path

from . import views


urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]

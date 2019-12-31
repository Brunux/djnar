from django.urls import path

from . import views


urlpatterns = [
    path('', views.ContactsView.as_view(), name='index'),
    path('items', views.ContactItemsView.as_view(), name='items'),
    path('create', views.ContactItemCreateView.as_view(), name='create'),
]

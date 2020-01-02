from django.urls import path

from . import views


urlpatterns = [
    path('', views.EventsView.as_view(), name='index'),
    path('items', views.EventItemsView.as_view(), name='items'),
    path('items-date', views.EventItemsDateView.as_view(), name='items_date'),
    path('create', views.EventItemCreateView.as_view(), name='create'),
    path('edit/<uuid:pid>',
         views.EventItemEditView.as_view(),
         name='edit')
]

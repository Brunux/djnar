from django.urls import path

from . import views


urlpatterns = [
    path('webcam', views.WebcamView.as_view(), name='webcam'),
    path('offer', views.OfferView.as_view(), name='offer'),
    # path('offer', views.offer, name='offer'),
]

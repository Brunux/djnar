from django.urls import path

from . import views


urlpatterns = [
    path('webcam', views.WebcamView.as_view(), name='webcam'),
    path('webcam/offer', views.WebcamOfferView.as_view(), name='webcam-offer'),
    path('server', views.ServerView.as_view(), name='server'),
    path('server/offer', views.ServerOfferView.as_view(), name='server-offer'),
]

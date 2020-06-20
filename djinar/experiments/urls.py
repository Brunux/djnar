from django.urls import path

from . import views


urlpatterns = [
    path('webcam', views.WebcamView.as_view(), name='webcam'),
    path('webcam/offer', views.WebcamOfferView.as_view(), name='webcam-offer'),
    path('streaming', views.StreamingView.as_view(), name='streaming'),
    path('streaming/offer', views.StreamingOfferView.as_view(), name='streaming-offer'),
]

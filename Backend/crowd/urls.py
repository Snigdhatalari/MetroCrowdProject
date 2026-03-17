# crowd/urls.py
from django.urls import path
from .views import predict_view, get_crowd_data

urlpatterns = [
    path('predict/', predict_view, name='predict'),
    path('crowd-data/', get_crowd_data, name='crowd_data'),
]
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('orm2', views.index2, name="index2"),
	path('initialize', views.make_data, name="make_data"),
]

from django.urls import path, include

from . import views

# Create Here
urlpatterns = [
    path("", views.index, name='index'),
]

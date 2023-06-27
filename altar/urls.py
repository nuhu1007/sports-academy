from django.urls import path, include

from . import views

# Create Here
urlpatterns = [
    # Authentication URLs
    path('login/', views.login, name='login'),


    path("", views.index, name='index'),

    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
]

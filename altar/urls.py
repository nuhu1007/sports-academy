from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

# Create Here
urlpatterns = [
    # Authentication URLs
    path('login/', views.login, name='login'),
    path('password-reset', views.ResetPasswordView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password-reset-confirm.html'), name='password-reset-confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password-reset-complete.html'), name='password_reset_complete'),
    path('verification', views.VerificationEmail.as_view(), name='verification'),


    path("", views.index, name='index'),

    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('add-player/', views.add_player, name='add_player'),
    path('players/', views.players_list, name='players'),
]

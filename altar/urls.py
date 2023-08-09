from django.urls import path
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
    path('logout/', views.logout, name='logout'),

    # Index URLs
    path("", views.index, name='index'),

    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),

    # Categories URLs
    path('categories/', views.categories, name='categories'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),

    # Branches URLs
    path('branches/', views.branches, name='branches'),
    path('delete_branch/<int:branch_id>/', views.delete_branch, name='delete_branch'),

    # Player URLs
    path('add-player/', views.add_player, name='add_player'),
    path('players/', views.players_list, name='players'),
    path('player-details/<int:player_id>/', views.player_details, name='player_details'),

    # Coach URLs
    path('coaches/', views.coaches_list, name='coaches'),

    # Training URLs
    path('training-management/', views.training_management, name='training_management'),
    path('training-details/<int:training_id>/', views.training_details, name='training_details'),

    # Attendance URLs
    path('attendance-management/', views.attendance_management, name='attendance_management'),
    path('record-attendance/<int:session_id>/', views.record_attendance, name='record_attendance'),

    # Game URLs
    path('game-schedule/', views.game_schedule, name='game_schedule'),
    path('game-details/<int:game_id>/', views.game_details, name='game_details'),
    path('match-results/', views.match_results, name='match_results'),
]

from django.urls import path
from django.contrib.auth import views as auth_views

from altar.views import attendance, authentication, branch, category, coaches, equipment, games, landing, players, training

# Create Here
urlpatterns = [
    # Authentication URLs
    path('login/', authentication.login, name='login'),
    path('password-reset', authentication.ResetPasswordView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password-reset-confirm.html'), name='password-reset-confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password-reset-complete.html'), name='password_reset_complete'),
    path('verification', authentication.VerificationEmail.as_view(), name='verification'),
    path('logout/', authentication.logout, name='logout'),

    # Index URLs
    path("", landing.index, name='index'),

    # Dashboard URLs
    path('dashboard/', landing.dashboard, name='dashboard'),

    # Categories URLs
    path('categories/', category.categories, name='categories'),
    path('delete_category/<int:category_id>/', category.delete_category, name='delete_category'),

    # Equipments URLs
    path('equipments/', equipment.equipments, name='equipments'),
    path('delete_equipment/<int:equipment_id>', equipment.delete_equipment, name='delete_equipment'),

    # Branches URLs
    path('branches/', branch.branches, name='branches'),
    path('delete_branch/<int:branch_id>/', branch.delete_branch, name='delete_branch'),

    # Player URLs
    path('add-player/', players.add_player, name='add_player'),
    path('players/', players.players_list, name='players'),
    path('player-details/<int:player_id>/', players.player_details, name='player_details'),

    # Coach URLs
    path('coaches/', coaches.CoachesView.as_view(), name='coaches'),
    path('coach/deactivate/<int:coach_id>/', coaches.DeactivateCoach.as_view(), name='deactivate_coach'),
    path('coach/reactivate/<int:coach_id>/', coaches.ReactivateCoach.as_view(), name='reactivate_coach'),

    # Training URLs
    path('training-management/', training.TrainingManagement.as_view(), name='training_management'),
    path('training_details/<int:training_id>/', training.training_details, name='training_details'),

    # Attendance URLs
    path('attendance-management/', attendance.AttendanceManagement.as_view(), name='attendance_management'),
    path('record_attendance/<int:session_id>/', attendance.record_attendance, name='record_attendance'),

    # Game URLs
    path('game-schedule/', games.game_schedule, name='game_schedule'),
    path('game-details/<int:game_id>/', games.game_details, name='game_details'),
    path('match-results/', games.match_results, name='match_results'),
]

from django.urls import path
from django.contrib.auth import views as auth_views

from altar.views import attendance, authentication, branch, category, coaches, equipment, games, landing, players, training

# Create Here
urlpatterns = [
    # Authentication URLs
    path('login/', authentication.LoginView.as_view(), name='login'),
    path('password-reset', authentication.ResetPasswordView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password-reset-confirm.html'), name='password-reset-confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password-reset-complete.html'), name='password_reset_complete'),
    path('verification', authentication.VerificationEmail.as_view(), name='verification'),
    path('logout/', authentication.LogoutView.as_view(), name='logout'),

    # Index URLs
    path("", landing.IndexView.as_view(), name='index'),

    # Dashboard URLs
    path('dashboard/', landing.DashboardView.as_view(), name='dashboard'),

    # Categories URLs
    path('categories/', category.CategoriesView.as_view(), name='categories'),
    path('delete-category/<int:category_id>', category.DeleteCategory.as_view(), name='delete_category'),

    # Equipments URLs
    path('equipments/', equipment.EquipmentsView.as_view(), name='equipments'),
    path('delete_equipment/<int:equipment_id>', equipment.DeleteEquipment.as_view(), name='delete_equipment'),

    # Branches URLs
    path('branches/', branch.BranchesView.as_view(), name='branches'),
    path('delete_branch/<int:branch_id>', branch.DeleteBranch.as_view(), name='delete_branch'),

    # Player URLs
    path('add-player/', players.AddPlayer.as_view(), name='add_player'),
    path('players/', players.PlayersList.as_view(), name='players'),
    path('player-details/<int:player_id>/', players.PlayerDetails.as_view(), name='player_details'),
    path('edit-player/<int:player_id>/', players.EditPlayer.as_view(), name='edit_player'),
    path('delete-player/<int:player_id>/', players.DeletePlayer.as_view(), name='delete_player'),

    # Coach URLs
    path('coaches/', coaches.CoachesView.as_view(), name='coaches'),
    path('coach/deactivate/<int:coach_id>/', coaches.DeactivateCoach.as_view(), name='deactivate_coach'),
    path('coach/reactivate/<int:coach_id>/', coaches.ReactivateCoach.as_view(), name='reactivate_coach'),

    # Training URLs
    path('training-management/', training.TrainingManagement.as_view(), name='training_management'),
    path('training_details/<int:training_id>/', training.TrainingDetails.as_view(), name='training_details'),

    # Attendance URLs
    path('attendance-management/', attendance.AttendanceManagement.as_view(), name='attendance_management'),
    path('record_attendance/<int:session_id>/', attendance.RecordAttendance.as_view(), name='record_attendance'),

    # Game URLs
    path('game-schedule/', games.game_schedule, name='game_schedule'),
    path('game-details/<int:game_id>/', games.game_details, name='game_details'),
    path('match-results/', games.match_results, name='match_results'),
]

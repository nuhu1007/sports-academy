from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from altar.models.branch import Branches
from altar.models.category import Categories
from altar.models.coaches import Coach
from altar.models.games import Game
from altar.models.players import Player
from altar.models.training import Attendance, TrainingSession
from altar.models.user import User

# Define classes here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'national_id', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number'),
        }),
    )


# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(TrainingSession)
admin.site.register(Player)
admin.site.register(Attendance)
admin.site.register(Categories)
admin.site.register(Game)
admin.site.register(Coach)
admin.site.register(Branches)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, OTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for the User model."""

    list_display = ('email', 'username',
                    'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """Admin configuration for the OTP model."""

    list_display = ('user', 'code', 'is_used', 'created_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'user__username', 'code')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

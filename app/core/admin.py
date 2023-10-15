"""
Django admin page specifications.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BasicUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BasicUserAdmin):
    """Admin page setup for users"""
    ordering = ['id']
    list_display = ['username', 'tier']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'tier')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'tier',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserImage)
admin.site.register(models.Tier)

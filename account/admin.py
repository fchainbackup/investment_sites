from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser,Profile

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_email_verified', 'nationality', 'phone_number'
        )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email','phone_number','nationality')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions','is_email_verified'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'nationality','phone_number')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser','is_email_verified',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        
    )
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
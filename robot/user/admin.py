from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    CUser,
    Address,
    OTPRequest
)
from .forms import CUserCreationForm



admin.site.register(OTPRequest)
admin.site.register(Address)

class CustomUserAdmin(BaseUserAdmin):
    """Custom admin interface for CUser model with phone number authentication."""
    
    add_form = CUserCreationForm
    ordering = ('id',)
    list_display = ('username', 'first_name', 'last_name', 
                    'is_active', 'phone_verified', 'email_verified')
    list_filter = ('is_active', 'is_superuser', 'phone_verified', 'email_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_editable = ('phone_verified', 'email_verified')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email', 'birthdate')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (_('Verification Status'), {'fields': ('phone_verified', 'email_verified')}),
        (_('Important Dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('last_login', 'created_at', 'updated_at')
    
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'email',
                    'is_active',
                ),
            },
        ),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Special handling for phone number display in admin"""
        form = super().get_form(request, obj, **kwargs)
        if 'username' in form.base_fields:
            form.base_fields['username'].label = _('Phone Number')
            form.base_fields['username'].help_text = _('Enter phone number in international format (+989...)')
        return form


admin.site.register(CUser, CustomUserAdmin)
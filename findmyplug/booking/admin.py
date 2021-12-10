from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Vehicle,Station,Review,Plug,Booking,Payment


# Register your models here.

class UserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'pincode', 'phone','is_staff','is_active']
    list_filter = ['email', 'pincode', 'phone','is_staff','is_active']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'pincode')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide,'),
            'fields': ('email', 'password1', 'password2', 'phone', 'pincode','is_staff','is_active'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Vehicle)
admin.site.register(Station)
admin.site.register(Review)
admin.site.register(Plug)
admin.site.register(Booking)
admin.site.register(Payment)
from django.contrib import admin
from .models import Client, Company, CustomUser, Booking, Event, CompanyCategory

@admin.register(CompanyCategory)
class CompanyCategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Customize the custom user admin if needed
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Customize the client admin if needed
    pass

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # Customize the company admin if needed
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # Customize the event admin if needed
    pass

def approve_bookings(modeladmin, request, queryset):
    queryset.update(approved=True)

class BookingAdmin(admin.ModelAdmin):
    list_display = ['client', 'event', 'queue_token', 'approved']
    actions = [approve_bookings]
admin.site.register(Booking, BookingAdmin)

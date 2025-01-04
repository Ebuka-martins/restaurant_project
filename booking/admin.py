# booking/admin.py
from django.contrib import admin
from .models import Table, Booking

# create your admin here
@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'booking_date', 'booking_time', 'number_of_guests')
    list_filter = ('booking_date', 'booking_time')
    search_fields = ('user__username', 'table__table_number')

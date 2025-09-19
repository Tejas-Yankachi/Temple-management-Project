from django.contrib import admin
from .models import (
    Temple, Event, EventRegistration, InventoryItem,
    RoomType, Room, Booking, Seva, SevaBooking,
    Pooja, PoojaBooking, Darshan, DarshanBooking,
    Donation, Festival
)

@admin.register(Temple)
class TempleAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'established_date', 'contact_number')
    search_fields = ('name', 'location')
    list_filter = ('established_date',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'temple', 'date', 'time', 'is_active')
    list_filter = ('is_active', 'date', 'temple')
    search_fields = ('name', 'description')

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rsvp', 'registered_at')
    list_filter = ('rsvp', 'registered_at')
    search_fields = ('user__username', 'event__name')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'temple', 'quantity', 'category', 'is_low_stock')
    list_filter = ('category', 'temple')
    search_fields = ('name', 'description')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'temple', 'bed_count', 'price_per_night', 'capacity')
    list_filter = ('temple', 'bed_count')
    search_fields = ('name', 'description')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'temple', 'room_type', 'status', 'floor')
    list_filter = ('status', 'room_type', 'temple')
    search_fields = ('room_number', 'notes')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'check_in', 'check_out')
    search_fields = ('user__username', 'room__room_number')

@admin.register(Seva)
class SevaAdmin(admin.ModelAdmin):
    list_display = ('name', 'temple', 'duration', 'amount', 'is_active')
    list_filter = ('is_active', 'temple')
    search_fields = ('name', 'description')

@admin.register(SevaBooking)
class SevaBookingAdmin(admin.ModelAdmin):
    list_display = ('devotee', 'seva', 'booking_date', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'booking_date')
    search_fields = ('devotee__username', 'seva__name')

@admin.register(Pooja)
class PoojaAdmin(admin.ModelAdmin):
    list_display = ('name', 'temple', 'duration', 'price', 'is_active')
    list_filter = ('is_active', 'temple')
    search_fields = ('name', 'description')

@admin.register(PoojaBooking)
class PoojaBookingAdmin(admin.ModelAdmin):
    list_display = ('devotee', 'pooja', 'booking_date', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'booking_date')
    search_fields = ('devotee__username', 'pooja__name')

@admin.register(Darshan)
class DarshanAdmin(admin.ModelAdmin):
    list_display = ('name', 'temple', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active', 'temple')
    search_fields = ('name', 'description')

@admin.register(DarshanBooking)
class DarshanBookingAdmin(admin.ModelAdmin):
    list_display = ('devotee', 'darshan', 'booking_date', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'booking_date')
    search_fields = ('devotee__username', 'darshan__name')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'temple', 'donation_amount', 'date_of_donation', 'receipt_issued')
    list_filter = ('receipt_issued', 'date_of_donation', 'temple')
    search_fields = ('donor_name', 'purpose')

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'temple', 'start_date', 'end_date', 'status', 'expected_attendance')
    list_filter = ('status', 'temple')
    search_fields = ('name', 'temple__name', 'description')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

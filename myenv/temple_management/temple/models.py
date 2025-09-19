from django.db import models

# Create your models here.
# temple/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Temple(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='temple_images/', blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    event_type = models.CharField(max_length=100, blank=True, null=True)
    special_guest_info = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} on {self.date}"

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rsvp = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    additional_guests = models.PositiveIntegerField(default=0)
    special_requirements = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} registration for {self.event.name}"

class InventoryItem(models.Model):
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='inventory')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    minimum_stock = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

    def is_low_stock(self):
        return self.quantity <= self.minimum_stock

class RoomType(models.Model):
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)
    bed_count = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=2)
    image = models.ImageField(upload_to='room_type_images/', blank=True, null=True)

    class Meta:
        unique_together = ('temple', 'name')

    def __str__(self):
        return f"{self.name} ({self.bed_count} beds)"

class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance'),
        ('unavailable', 'Unavailable'),
    ]
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    notes = models.TextField(blank=True)
    floor = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('temple', 'room_number')

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type.name} ({self.status})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    special_requests = models.TextField(blank=True, null=True)
    
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    payment_status = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking for {self.user.username} in {self.room.room_number} from {self.check_in} to {self.check_out}"

class Seva(models.Model):
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='sevas')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    max_devotees_per_day = models.PositiveIntegerField(default=10)
    image = models.ImageField(upload_to='seva_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SevaBooking(models.Model):
    devotee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seva_bookings')
    seva = models.ForeignKey(Seva, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.devotee.username} - {self.seva.name} on {self.booking_date}"

class Darshan(models.Model):
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='darshans')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_capacity = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='darshan_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class DarshanBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    PREFERRED_TIME_SLOTS = [
        ('morning', 'Morning (6 AM - 9 AM)'),
        ('midday', 'Midday (12 PM - 2 PM)'),
        ('evening', 'Evening (5 PM - 8 PM)'),
    ]
    
    darshan = models.ForeignKey(Darshan, on_delete=models.CASCADE, related_name='bookings')
    devotee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='darshan_bookings')
    booking_date = models.DateField()
    preferred_time_slot = models.CharField(max_length=20, choices=PREFERRED_TIME_SLOTS)
    number_of_people = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.devotee.username} - {self.darshan.name} on {self.booking_date}"

class Donation(models.Model):
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='donations')
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    donor_name = models.CharField(max_length=100)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_donation = models.DateField()
    purpose = models.CharField(max_length=200, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_issued = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.donor_name} - {self.donation_amount} on {self.date_of_donation}"

class Festival(models.Model):
    name = models.CharField(max_length=200)
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='festivals')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(default='23:59')
    image = models.ImageField(upload_to='festivals/', null=True, blank=True)
    expected_attendance = models.IntegerField(default=100)
    status = models.CharField(max_length=20, choices=[
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FestivalBooking(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='festival_bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s booking for {self.festival.name}"

    class Meta:
        ordering = ['-booking_date']

class Pooja(models.Model):
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='poojas')
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    benefits = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='pooja_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PoojaBooking(models.Model):
    pooja = models.ForeignKey(Pooja, on_delete=models.CASCADE, related_name='bookings')
    devotee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pooja_bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    number_of_people = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.devotee.username} - {self.pooja.name} on {self.booking_date}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username}'s profile"
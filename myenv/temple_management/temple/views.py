from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.contrib.auth import login, authenticate
from django.utils import timezone
from datetime import timedelta
from .models import (
    Temple, Event, EventRegistration, Room, RoomType, Booking,
    Seva, SevaBooking, Pooja, PoojaBooking, Darshan, DarshanBooking,
    Donation, Festival, FestivalBooking, UserProfile
)
from .forms import (
    UserRegistrationForm, EventRegistrationForm, RoomBookingForm, SevaBookingForm,
    PoojaBookingForm, DarshanBookingForm, DonationForm, UserLoginForm, TempleForm,
    FestivalBookingForm
)

def home(request):
    temples = Temple.objects.all()[:6]
    events = Event.objects.filter(is_active=True)[:4]
    festivals = Festival.objects.filter(status='upcoming')[:4]
    return render(request, 'temple/home.html', {
        'temples': temples,
        'events': events,
        'festivals': festivals
    })

# Temple Views
def temple_list(request):
    temples = Temple.objects.all()
    temple_id = request.GET.get('temple_id')
    search_query = request.GET.get('search')
    if temple_id:
        temples = temples.filter(id=temple_id)
    if search_query:
        temples = temples.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    return render(request, 'temple/temple_list.html', {'temples': temples})

def temple_detail(request, pk):
    temple = get_object_or_404(Temple, pk=pk)
    events = temple.events.filter(is_active=True)
    sevas = temple.sevas.filter(is_active=True)
    poojas = temple.poojas.filter(is_active=True)
    return render(request, 'temple/temple_detail.html', {
        'temple': temple,
        'events': events,
        'sevas': sevas,
        'poojas': poojas
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def temple_edit(request, pk):
    temple = get_object_or_404(Temple, pk=pk)
    if request.method == 'POST':
        form = TempleForm(request.POST, request.FILES, instance=temple)
        if form.is_valid():
            form.save()
            messages.success(request, 'Temple information updated successfully!')
            return redirect('temple_detail', pk=temple.pk)
    else:
        form = TempleForm(instance=temple)
    return render(request, 'temple/temple_edit.html', {
        'form': form,
        'temple': temple
    })

# Event Views
def event_list(request):
    events = Event.objects.filter(is_active=True)
    return render(request, 'temple/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'temple/event_detail.html', {'event': event})

@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            messages.success(request, 'Successfully registered for the event!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventRegistrationForm()
    return render(request, 'temple/event_register.html', {'form': form, 'event': event})

# Room Views
def room_list(request):
    rooms = Room.objects.filter(status='available')
    return render(request, 'temple/room_list.html', {'rooms': rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'temple/room_detail.html', {'room': room})

@login_required
def room_book(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Check if room is available
    if room.status != 'available':
        messages.error(request, 'This room is not available for booking.')
        return redirect('room_detail', room_id=room.id)
    
    if request.method == 'POST':
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            
            # Validate dates
            if check_out <= check_in:
                messages.error(request, 'Check-out date must be after check-in date.')
                return render(request, 'temple/room_book.html', {'form': form, 'room': room})
            
            # Check if room is already booked for these dates
            existing_bookings = Booking.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in,
                status__in=['confirmed', 'pending']
            )
            
            if existing_bookings.exists():
                messages.error(request, 'This room is already booked for the selected dates.')
                return render(request, 'temple/room_book.html', {'form': form, 'room': room})
            
            # Calculate total amount
            nights = (check_out - check_in).days
            total_amount = room.room_type.price_per_night * nights
            
            # Create booking
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.total_amount = total_amount
            booking.status = 'pending'
            booking.save()
            
            messages.success(request, 'Your room booking request has been submitted successfully.')
            return redirect('user_bookings')
    else:
        form = RoomBookingForm()
    
    return render(request, 'temple/room_book.html', {'form': form, 'room': room})

# Booking Views
@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'temple/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'temple/booking_detail.html', {'booking': booking})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check if the booking belongs to the current user
    if booking.user != request.user:
        messages.error(request, 'You are not authorized to cancel this booking.')
        return redirect('user_bookings')
    
    # Check if the booking is in a cancellable state
    if booking.status != 'pending':
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('booking_detail', pk=booking.id)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking has been cancelled successfully.')
        return redirect('user_bookings')
    
    return render(request, 'temple/booking_cancel_confirm.html', {'booking': booking})

# Seva Views
def seva_list(request):
    sevas = Seva.objects.filter(is_active=True)
    temples = Temple.objects.all()
    search_query = request.GET.get('search')
    temple_id = request.GET.get('temple')
    if temple_id:
        sevas = sevas.filter(temple_id=temple_id)
    if search_query:
        sevas = sevas.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    return render(request, 'temple/seva_list.html', {'sevas': sevas, 'temples': temples})

def seva_detail(request, pk):
    seva = get_object_or_404(Seva, pk=pk)
    return render(request, 'temple/seva_detail.html', {'seva': seva})

@login_required
def seva_book(request, pk):
    seva = get_object_or_404(Seva, pk=pk)
    if request.method == 'POST':
        form = SevaBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.seva = seva
            booking.devotee = request.user
            booking.amount = seva.amount
            booking.save()
            messages.success(request, 'Seva booked successfully!')
            return redirect('seva_detail', pk=seva.pk)
    else:
        form = SevaBookingForm()
    return render(request, 'temple/seva_book.html', {'form': form, 'seva': seva})

@login_required
def seva_booking_detail(request, pk):
    booking = get_object_or_404(SevaBooking, pk=pk, devotee=request.user)
    return render(request, 'temple/seva_booking_detail.html', {'booking': booking})

# Pooja Views
def pooja_list(request):
    poojas = Pooja.objects.filter(is_active=True)
    temples = Temple.objects.all()
    search_query = request.GET.get('search')
    temple_id = request.GET.get('temple')
    if temple_id:
        poojas = poojas.filter(temple_id=temple_id)
    if search_query:
        poojas = poojas.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    return render(request, 'temple/pooja_list.html', {
        'poojas': poojas,
        'temples': temples
    })

def pooja_detail(request, pk):
    pooja = get_object_or_404(Pooja, pk=pk)
    return render(request, 'temple/pooja_detail.html', {'pooja': pooja})

@login_required
def pooja_book(request, pk):
    pooja = get_object_or_404(Pooja, pk=pk)
    if request.method == 'POST':
        form = PoojaBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.pooja = pooja
            booking.devotee = request.user
            booking.amount_paid = pooja.price
            booking.save()
            messages.success(request, 'Pooja booked successfully!')
            return redirect('pooja_detail', pk=pooja.pk)
    else:
        form = PoojaBookingForm()
    return render(request, 'temple/pooja_book.html', {'form': form, 'pooja': pooja})

# Darshan Views
def darshan_list(request):
    darshans = Darshan.objects.filter(is_active=True)
    search_query = request.GET.get('search')
    date_query = request.GET.get('date')
    if search_query:
        darshans = darshans.filter(
            temple__name__icontains=search_query
        )
    if date_query:
        darshans = darshans.filter(
            # Assuming you have a date field, otherwise adjust accordingly
            # For now, let's assume you want to filter by a related date field if it exists
        )
    return render(request, 'temple/darshan_list.html', {'darshans': darshans})

def darshan_detail(request, pk):
    darshan = get_object_or_404(Darshan, pk=pk)
    return render(request, 'temple/darshan_detail.html', {'darshan': darshan})

@login_required
def darshan_book(request, pk):
    darshan = get_object_or_404(Darshan, pk=pk)
    if request.method == 'POST':
        form = DarshanBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.darshan = darshan
            booking.devotee = request.user
            booking.save()
            messages.success(request, 'Darshan booked successfully!')
            return redirect('darshan_detail', pk=darshan.pk)
    else:
        form = DarshanBookingForm()
    return render(request, 'temple/darshan_book.html', {'form': form, 'darshan': darshan})

# Donation Views
def donation_list(request):
    donations = Donation.objects.all()
    return render(request, 'temple/donation_list.html', {'donations': donations})

@login_required
def donation_create(request):
    if request.method == 'POST':
        try:
            temple_id = request.POST.get('temple')
            if not temple_id:
                messages.error(request, 'Please select a temple.')
                return redirect('donation_create')
            
            temple_instance = get_object_or_404(Temple, id=temple_id)
            
            donation_amount_str = request.POST.get('donation_amount')
            if not donation_amount_str:
                messages.error(request, 'Donation amount is required.')
                return redirect('donation_create')
            try:
                donation_amount_val = float(donation_amount_str)
                if donation_amount_val <= 0:
                    raise ValueError("Donation amount must be positive.")
            except ValueError:
                messages.error(request, 'Invalid donation amount.')
                return redirect('donation_create')

            donation = Donation(
                donor=request.user,
                donor_name=request.user.get_full_name() if request.user.get_full_name() else request.user.username,
                temple=temple_instance,
                donation_amount=donation_amount_val,
                purpose=request.POST.get('purpose', ''),
                payment_method=request.POST.get('payment_method', ''),
                notes=request.POST.get('notes', ''),
                date_of_donation=timezone.now().date()
            )
            donation.save()
            messages.success(request, 'Donation request submitted successfully!')
            return redirect('user_donations')
        except Temple.DoesNotExist:
            messages.error(request, 'Selected temple does not exist.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        return redirect('donation_create')
    
    temples = Temple.objects.all()
    return render(request, 'temple/donation_create.html', {
        'temples': temples
    })

@login_required
def donation_detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    return render(request, 'temple/donation_detail.html', {'donation': donation})

# Festival Views
def festival_list(request):
    festivals = Festival.objects.all()
    search_query = request.GET.get('search')
    date_query = request.GET.get('date')
    if search_query:
        festivals = festivals.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if date_query:
        festivals = festivals.filter(
            start_date__lte=date_query,
            end_date__gte=date_query
        )
    return render(request, 'temple/festival_list.html', {'festivals': festivals})

def festival_detail(request, pk):
    festival = get_object_or_404(Festival, pk=pk)
    return render(request, 'temple/festival_detail.html', {'festival': festival})

@login_required
def festival_book(request, pk):
    festival = get_object_or_404(Festival, pk=pk)
    
    if request.method == 'POST':
        form = FestivalBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.festival = festival
            booking.save()
            messages.success(request, 'Festival booking successful!')
            return redirect('festival_booking_detail', pk=booking.pk)
    else:
        form = FestivalBookingForm()
    
    return render(request, 'temple/festival_book.html', {
        'form': form,
        'festival': festival
    })

@login_required
def festival_booking_detail(request, pk):
    booking = get_object_or_404(FestivalBooking, pk=pk, user=request.user)
    return render(request, 'temple/festival_booking_detail.html', {
        'booking': booking
    })

# User Profile Views
@login_required
def profile(request):
    return render(request, 'temple/profile.html')

@login_required
def user_bookings(request):
    room_bookings = Booking.objects.filter(user=request.user)
    seva_bookings = SevaBooking.objects.filter(devotee=request.user)
    pooja_bookings = PoojaBooking.objects.filter(devotee=request.user)
    darshan_bookings = DarshanBooking.objects.filter(devotee=request.user)
    return render(request, 'temple/user_bookings.html', {
        'room_bookings': room_bookings,
        'seva_bookings': seva_bookings,
        'pooja_bookings': pooja_bookings,
        'darshan_bookings': darshan_bookings
    })

@login_required
def user_donations(request):
    donations = Donation.objects.filter(donor=request.user)
    return render(request, 'temple/user_donations.html', {'donations': donations})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Temple Management System.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'temple/register.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                return render(request, 'temple/login.html', {'form': form, 'error': 'Invalid username or password.'})
        else:
            return render(request, 'temple/login.html', {'form': form, 'error': 'Invalid form submission.'})
    else:
        form = UserLoginForm()
        return render(request, 'temple/login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Get basic statistics
    total_temples = Temple.objects.count()
    total_donations = Donation.objects.aggregate(total=Sum('donation_amount'))['total'] or 0
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()
    
    # Get recent activities
    recent_donations = Donation.objects.order_by('-date_of_donation')[:5]
    recent_bookings = Booking.objects.order_by('-date')[:5]
    
    # Get monthly statistics
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)
    
    monthly_donations = Donation.objects.filter(
        date_of_donation__gte=thirty_days_ago
    ).aggregate(total=Sum('donation_amount'))['total'] or 0
    
    monthly_bookings = Booking.objects.filter(
        date__gte=thirty_days_ago
    ).count()
    
    # Get service statistics
    seva_bookings = SevaBooking.objects.count()
    pooja_bookings = PoojaBooking.objects.count()
    darshan_bookings = DarshanBooking.objects.count()
    
    # Get room statistics
    available_rooms = Room.objects.filter(status='available').count()
    occupied_rooms = Room.objects.filter(status='occupied').count()
    
    # Get upcoming events and festivals
    upcoming_events = Event.objects.filter(
        date__gte=today,
        is_active=True
    ).order_by('date')[:5]
    
    upcoming_festivals = Festival.objects.filter(
        date__gte=today,
        status='upcoming'
    ).order_by('date')[:5]
    
    # Get popular services
    popular_sevas = Seva.objects.annotate(
        booking_count=Count('sevabooking')
    ).order_by('-booking_count')[:5]
    
    popular_poojas = Pooja.objects.annotate(
        booking_count=Count('poojabooking')
    ).order_by('-booking_count')[:5]
    
    context = {
        # Basic statistics
        'total_temples': total_temples,
        'total_donations': total_donations,
        'total_bookings': total_bookings,
        'total_users': total_users,
        
        # Monthly statistics
        'monthly_donations': monthly_donations,
        'monthly_bookings': monthly_bookings,
        
        # Service statistics
        'seva_bookings': seva_bookings,
        'pooja_bookings': pooja_bookings,
        'darshan_bookings': darshan_bookings,
        
        # Room statistics
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        
        # Recent activities
        'recent_donations': recent_donations,
        'recent_bookings': recent_bookings,
        
        # Upcoming events
        'upcoming_events': upcoming_events,
        'upcoming_festivals': upcoming_festivals,
        
        # Popular services
        'popular_sevas': popular_sevas,
        'popular_poojas': popular_poojas,
    }
    
    return render(request, 'temple/admin/dashboard.html', context)

@login_required
def user_dashboard(request):
    # Get user's bookings
    room_bookings = Booking.objects.filter(user=request.user).order_by('-date')[:5]
    seva_bookings = SevaBooking.objects.filter(devotee=request.user).order_by('-booking_date')[:5]
    pooja_bookings = PoojaBooking.objects.filter(devotee=request.user).order_by('-booking_date')[:5]
    darshan_bookings = DarshanBooking.objects.filter(devotee=request.user).order_by('-booking_date')[:5]
    
    # Get user's donations
    donations = Donation.objects.filter(donor=request.user).order_by('-date')[:5]
    
    # Get upcoming events
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now(),
        is_active=True
    ).order_by('date')[:5]
    
    # Get upcoming festivals
    upcoming_festivals = Festival.objects.filter(
        date__gte=timezone.now(),
        status='upcoming'
    ).order_by('date')[:5]
    
    context = {
        'room_bookings': room_bookings,
        'seva_bookings': seva_bookings,
        'pooja_bookings': pooja_bookings,
        'darshan_bookings': darshan_bookings,
        'donations': donations,
        'upcoming_events': upcoming_events,
        'upcoming_festivals': upcoming_festivals,
    }
    
    return render(request, 'temple/user_dashboard.html', context)


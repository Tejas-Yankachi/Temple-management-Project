from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.admin_login, name='login'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    
    # Dashboard URLs
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    
    # Temple URLs
    path('temples/', views.temple_list, name='temple_list'),
    path('temples/<int:pk>/', views.temple_detail, name='temple_detail'),
    path('temples/<int:pk>/edit/', views.temple_edit, name='temple_edit'),
    
    # Event URLs
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/register/', views.event_register, name='event_register'),
    
    # Room URLs
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', views.room_book, name='room_book'),
    
    # Booking URLs
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # Seva URLs
    path('sevas/', views.seva_list, name='seva_list'),
    path('sevas/<int:pk>/', views.seva_detail, name='seva_detail'),
    path('sevas/<int:pk>/book/', views.seva_book, name='seva_book'),
    path('seva-bookings/<int:pk>/', views.seva_booking_detail, name='seva_booking_detail'),
    
    # Pooja URLs
    path('poojas/', views.pooja_list, name='pooja_list'),
    path('poojas/<int:pk>/', views.pooja_detail, name='pooja_detail'),
    path('poojas/<int:pk>/book/', views.pooja_book, name='pooja_book'),
    
    # Darshan URLs
    path('darshans/', views.darshan_list, name='darshan_list'),
    path('darshans/<int:pk>/', views.darshan_detail, name='darshan_detail'),
    path('darshans/<int:pk>/book/', views.darshan_book, name='darshan_book'),
    
    # Donation URLs
    path('donations/', views.donation_list, name='donation_list'),
    path('donations/create/', views.donation_create, name='donation_create'),
    path('donations/<int:pk>/', views.donation_detail, name='donation_detail'),
    
    # Festival URLs
    path('festivals/', views.festival_list, name='festival_list'),
    path('festivals/<int:pk>/', views.festival_detail, name='festival_detail'),
    path('festivals/<int:pk>/book/', views.festival_book, name='festival_book'),
    path('festival-bookings/<int:pk>/', views.festival_booking_detail, name='festival_booking_detail'),
    
    # User Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/bookings/', views.user_bookings, name='user_bookings'),
    path('profile/donations/', views.user_donations, name='user_donations'),
]
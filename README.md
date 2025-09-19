# Temple Management System

A comprehensive web application for managing temple activities, bookings, and services. Built with Django and modern web technologies.

## Features

- Temple Management
  - Multiple temple profiles
  - Temple details and information
  - Image gallery
  - Contact information

- Event Management
  - Create and manage temple events
  - Event registration
  - Event details and schedules

- Room Booking System
  - Room types and availability
  - Online booking
  - Booking management
  - Payment integration

- Seva and Pooja Services
  - Book various sevas
  - Schedule poojas
  - Service details and pricing
  - Online payment

- Darshan Booking
  - Time slot booking
  - Queue management
  - Special darshan options

- Donation System
  - Online donations
  - Donation tracking
  - Receipt generation

- Festival Management
  - Festival calendar
  - Special events
  - Festival details

- User Management
  - User registration and authentication
  - Profile management
  - Booking history
  - Donation history

## Technology Stack

- Backend: Django 5.0
- Frontend: HTML5, CSS3, JavaScript, Bootstrap 5
- Database: SQLite (development) / PostgreSQL (production)
- Additional Packages:
  - django-crispy-forms
  - Pillow
  - django-allauth
  - django-rest-framework
  - And more (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/temple-management.git
cd temple-management
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
temple_management/
├── manage.py
├── requirements.txt
├── temple_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── temple/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   └── temple/
│       ├── home.html
│       └── ...
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── media/
    ├── temple_images/
    ├── event_images/
    └── ...
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@templemanagement.com or create an issue in the repository.

## Acknowledgments

- Django Documentation
- Bootstrap Documentation
- Font Awesome
- Unsplash for images 

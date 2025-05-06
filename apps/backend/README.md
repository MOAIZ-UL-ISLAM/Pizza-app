# JWT Authentication API

A robust Django REST API with JWT authentication using Djoser and PostgreSQL. Includes user registration, login, and password reset with OTP functionality.

## Features

- JWT-based authentication
- User registration with email and username
- Login with email and password
- Password reset via OTP sent to email
- Rate limiting for API endpoints
- Custom user model
- Role-based permissions
- PostgreSQL database integration
- Senior-level project structure

## Project Structure

```
auth_project/
├── accounts/                  # User authentication app
│   ├── admin.py               # Admin panel configuration
│   ├── apps.py                # App configuration
│   ├── email_templates/       # Email templates for password reset
│   ├── management/            # Management commands
│   ├── models.py              # User and OTP models
│   ├── permissions.py         # Custom permissions
│   ├── serializers.py         # API serializers
│   ├── signals.py             # Signal handlers
│   ├── tasks.py               # Async tasks (for future expansion)
│   ├── urls.py                # API routes
│   └── views.py               # API views
├── auth_project/              # Main project directory
│   ├── asgi.py                # ASGI configuration
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── common/                    # Shared code
│   ├── exceptions.py          # Custom exception handlers
│   ├── mixins.py              # Reusable view mixins
│   └── utils.py               # Utility functions
├── manage.py                  # Django management script
├── requirements.txt           # Project dependencies
└── .env.example               # Environment variables template
```

## Requirements

- Python 3.10+
- PostgreSQL 14+
- Django 5.0+

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd auth_project
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and fill in your configurations:
   ```
   cp .env.example .env
   ```

5. Create the PostgreSQL database:
   ```
   createdb auth_db
   ```

6. Run migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser_with_password --email admin@example.com --username admin --password 12345678
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- `POST /api/auth/users/` - Register a new user
- `POST /api/auth/jwt/create/` - Login and obtain JWT tokens
- `POST /api/auth/jwt/refresh/` - Refresh JWT token
- `POST /api/auth/jwt/verify/` - Verify JWT token
- `GET /api/auth/me/` - Get current user details
- `PATCH /api/auth/me/` - Update current user details

### Password Reset

- `POST /api/auth/password/reset/` - Request password reset (sends OTP to email)
- `POST /api/auth/password/reset/verify-otp/` - Verify OTP code
- `POST /api/auth/password/reset/confirm/` - Set new password after OTP verification

## Swagger Documentation

API documentation is available at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Password Requirements

- Must be exactly 8 digits
- Cannot be a common password
- Cannot be similar to user attributes

## Rate Limiting

The API implements rate limiting to prevent abuse:
- Anonymous users: 100 requests per day
- Authenticated users: 1000 requests per day
- Authentication endpoints: 3 requests per minute
- Password reset: 3 requests per hour

## Development

### Running Tests

```
python manage.py test
```

### Code Style

Follow PEP 8 guidelines for Python code styling.

## License

This project is licensed under the MIT License.
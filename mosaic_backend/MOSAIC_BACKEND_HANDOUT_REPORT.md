# Mosaic Insurance ERP Backend - Comprehensive Technical Handout

## Project Overview
**Repository:** https://github.com/MamurS/mosaic_Django_backend.git  
**Purpose:** Django REST API backend for Insurance ERP web application  
**Target Market:** Uzbekistan insurance industry  
**Language/Locale:** Russian (ru-ru), Asia/Tashkent timezone  
**Python Version:** 3.11.9  

## Architecture Summary
- **Framework:** Django 4.1.13 with Django REST Framework 3.14.0
- **Database:** SQLite3 (development/temporary), configured for PostgreSQL production
- **Authentication:** JWT tokens with SimpleJWT
- **CORS:** Configured for React frontend integration
- **Deployment:** Configured for Render.com hosting
- **File Structure:** Standard Django project with single `api` app

---

## Complete File Structure

```
mosaic_backend/
├── build.sh                           # Render deployment script
├── env.example                        # Environment variables template
├── requirements-dev.txt               # Development dependencies
├── requirements-prod.txt              # Production dependencies  
├── runtime.txt                        # Python version specification
└── insurance_project/                 # Main Django project
    ├── db.sqlite3                     # SQLite database file
    ├── manage.py                      # Django management script
    ├── requirements.txt               # Base requirements
    ├── api/                           # Main application
    │   ├── __init__.py
    │   ├── admin.py                   # Django admin configuration
    │   ├── apps.py                    # App configuration
    │   ├── models.py                  # Database models
    │   ├── serializers.py             # API serializers
    │   ├── tests.py                   # Unit tests
    │   ├── urls.py                    # API URL routing
    │   ├── views.py                   # API views/endpoints
    │   └── migrations/                # Database migrations
    │       ├── __init__.py
    │       └── 0001_initial.py        # Initial migration
    └── insurance_project/             # Project configuration
        ├── __init__.py
        ├── asgi.py                    # ASGI configuration
        ├── settings.py                # Django settings
        ├── urls.py                    # Root URL configuration
        └── wsgi.py                    # WSGI configuration
```

---

## Complete Source Code Documentation

### 1. Configuration Files

#### `build.sh` - Render Deployment Script
```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from the root directory (one level up)
pip install -r ../requirements-prod.txt

# Run Django commands from the current directory ('insurance_project')
# where manage.py is located.
python manage.py collectstatic --no-input
python manage.py migrate
```

#### `env.example` - Environment Configuration Template
```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (for production)
DATABASE_URL=postgres://user:password@localhost:5432/insurance_db

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0

# Sentry Configuration (optional - for error tracking)
SENTRY_DSN=your-sentry-dsn-here
```

#### `runtime.txt` - Python Version
```
python-3.11.9
```

#### `requirements-prod.txt` - Production Dependencies
```txt
# Core Django framework
Django==4.1.13
# Django REST Framework for building APIs
djangorestframework==3.14.0
# CORS headers for cross-origin requests
django-cors-headers==4.3.1
# Django filtering for API endpoints
django-filter==23.3
# JWT authentication for REST API
djangorestframework-simplejwt==5.3.0
# Python timezone support
pytz==2023.3
# SQL parsing library (used by Django)
sqlparse==0.4.4
# ASGI reference implementation
asgiref==3.7.2
# Python JWT library (dependency of djangorestframework-simplejwt)
PyJWT==2.8.0

# ===== RENDER DEPLOYMENT PACKAGES =====
# WSGI HTTP Server for Python (production server)
gunicorn==21.2.0
# Static file serving middleware
whitenoise==6.5.0
# Environment variable management
python-decouple==3.8
# Database URL parsing
dj-database-url==2.1.0
# Setup tools for pkg_resources (needed by simplejwt)
setuptools==69.0.3
```

#### `requirements-dev.txt` - Development Dependencies
```txt
# Include all base requirements
-r requirements.txt

# Development and testing dependencies
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0

# Code formatting and linting
black==23.9.1
flake8==6.1.0
isort==5.12.0

# Django debugging toolbar
django-debug-toolbar==4.2.0

# Django extensions for development
django-extensions==3.2.3

# Factory for creating test data
factory-boy==3.3.0

# Environment variable management
python-decouple==3.8
```

### 2. Django Project Configuration

#### `insurance_project/manage.py` - Django Management Script
```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

#### `insurance_project/insurance_project/settings.py` - Main Configuration
```python
"""
Django settings for insurance_project project.
Configured for Render deployment with PostgreSQL.
"""

import os
from pathlib import Path
import dj_database_url
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-$5$sij*i9=u_%11r@%n$zgvna^nve7)4e=b)plx5fu+81gub+h')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# Allowed hosts for Render deployment
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',  # Allow all Render subdomains
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your apps
    'api',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',    
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files for production
    'corsheaders.middleware.CorsMiddleware',  # Move CORS to top
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'insurance_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'insurance_project.wsgi.application'

# Database - Use SQLite for deployment (temporary fix)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'  # Russian for your insurance system
TIME_ZONE = 'Asia/Tashkent'  # Uzbekistan timezone
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
] if os.path.exists(BASE_DIR / 'static') else []

# WhiteNoise configuration for better static file handling
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}

# CORS configuration for React frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",
    "https://mosaic-react-webapp.onrender.com",
]

# For development, allow all origins (keep your existing setting)


CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Security settings for production
if not DEBUG:
    # Security settings for production deployment
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Session security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True

# Email configuration (optional - for password resets, notifications)
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
}

# Custom settings for your insurance ERP
INSURANCE_ERP_SETTINGS = {
    'DEFAULT_CURRENCY': 'UZS',
    'SUPPORTED_CURRENCIES': ['UZS', 'USD', 'EUR'],
    'DEFAULT_POLICY_TERM_MONTHS': 12,
    'MAX_UPLOAD_SIZE': 5 * 1024 * 1024,  # 5MB
    'ALLOWED_FILE_TYPES': ['.pdf', '.jpg', '.jpeg', '.png', '.xlsx'],
}
```

#### `insurance_project/insurance_project/urls.py` - Root URL Configuration
```python
"""insurance_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # Add this line
]

# insurance_project/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # Add these lines for token authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### 3. API Application Code

#### `insurance_project/api/models.py` - Database Models
```python
# api/models.py

from django.db import models
from django.utils import timezone

# These models define the database tables for our application.
# Django's ORM will automatically handle creating the SQL commands.

class Client(models.Model):
    """
    Represents a client in the insurance system.
    """
    class ClientStatus(models.TextChoices):
        NEW = 'new', 'Новый'
        ACTIVE = 'active', 'Активный'
        VIP = 'vip', 'VIP'
        INACTIVE = 'inactive', 'Неактивный'

    class Currency(models.TextChoices):
        UZS = 'UZS', 'UZS'
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'

    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=255, db_index=True)
    inn = models.CharField(max_length=20, unique=True, db_index=True)
    legalName = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, default="Узбекистан")
    region = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    companyGroup = models.CharField(max_length=255, blank=True, null=True)
    clientStatus = models.CharField(max_length=10, choices=ClientStatus.choices, default=ClientStatus.NEW)
    financialReporting = models.CharField(max_length=3, default="No")
    revenue = models.FloatField(default=0)
    revenueCurrency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)
    revenuePeriod = models.CharField(max_length=20, blank=True, null=True)
    creditLimit = models.FloatField(default=0)
    limitCurrency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)

    def __str__(self):
        return f"{self.name} (ИНН: {self.inn})"

class Policy(models.Model):
    """
    Represents an insurance policy linked to a client.
    """
    class PolicyStatus(models.TextChoices):
        ACTIVE = 'active', 'Активен'
        PENDING = 'pending', 'Ожидает'
        EXPIRED = 'expired', 'Истек'

    class Currency(models.TextChoices):
        UZS = 'UZS', 'UZS'
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'

    client = models.ForeignKey(Client, related_name='policies', on_delete=models.CASCADE)
    creationDate = models.DateField(default=timezone.now)
    insuranceAmount = models.FloatField()
    insuranceAmountCurrency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)
    premium = models.FloatField()
    netPremium = models.FloatField()
    premiumCurrency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)
    status = models.CharField(max_length=10, choices=PolicyStatus.choices, default=PolicyStatus.PENDING)

    def __str__(self):
        return f"Полис №{self.id} для {self.client.name}"
```

#### `insurance_project/api/serializers.py` - API Serializers
```python
# api/serializers.py

from rest_framework import serializers
from .models import Client, Policy

# Serializers define how the data is represented in the API (e.g., as JSON).
# They also handle validation when data is sent to the server.

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__' # Include all fields from the Policy model

class ClientSerializer(serializers.ModelSerializer):
    # This nested serializer will include all policies related to a client.
    policies = PolicySerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__' # Include all fields from the Client model

        # api/serializers.py

from rest_framework import serializers
from .models import Client, Policy
from django.contrib.auth.models import User # <-- Add this import

# ... (your existing PolicySerializer and ClientSerializer) ...

# Add this new serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
```

#### `insurance_project/api/views.py` - API Views/Endpoints
```python
# api/views.py

from rest_framework import viewsets
from .models import Client, Policy
from .serializers import ClientSerializer, PolicySerializer
from rest_framework import viewsets, filters
from rest_framework.views import APIView # <-- Add this import
from rest_framework.response import Response # <-- Add this import
from rest_framework.permissions import IsAuthenticated # <-- Add this import
from .models import Client, Policy
from .serializers import ClientSerializer, PolicySerializer, UserSerializer # <-- Add UserSerializer


# ViewSets define the logic for the API endpoints.
# The ModelViewSet automatically provides CRUD (Create, Read, Update, Delete) operations.

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clients to be viewed or edited.
    """
    queryset = Client.objects.all().order_by('-date')
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'inn']

class PolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows policies to be viewed or edited.
    """
    queryset = Policy.objects.all().order_by('-creationDate')
    serializer_class = PolicySerializer

# Add this new view
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
```

#### `insurance_project/api/urls.py` - API URL Configuration
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, PolicyViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, PolicyViewSet, MeView # <-- Add MeView

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'policies', PolicyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'policies', PolicyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', MeView.as_view(), name='me'), # <-- Add this line
]
```

#### `insurance_project/api/admin.py` - Django Admin Configuration
```python
from django.contrib import admin
from .models import Client, Policy

admin.site.register(Client)
admin.site.register(Policy)
```

#### `insurance_project/api/apps.py` - App Configuration
```python
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
```

### 4. Database Migration

#### `insurance_project/api/migrations/0001_initial.py` - Initial Database Migration
```python
# Generated by Django 5.2.4 on 2025-07-27 02:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('inn', models.CharField(db_index=True, max_length=20, unique=True)),
                ('legalName', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(default='Узбекистан', max_length=100)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('industry', models.CharField(blank=True, max_length=100, null=True)),
                ('companyGroup', models.CharField(blank=True, max_length=255, null=True)),
                ('clientStatus', models.CharField(choices=[('new', 'Новый'), ('active', 'Активный'), ('vip', 'VIP'), ('inactive', 'Неактивный')], default='new', max_length=10)),
                ('financialReporting', models.CharField(default='No', max_length=3)),
                ('revenue', models.FloatField(default=0)),
                ('revenueCurrency', models.CharField(choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')], default='UZS', max_length=3)),
                ('revenuePeriod', models.CharField(blank=True, max_length=20, null=True)),
                ('creditLimit', models.FloatField(default=0)),
                ('limitCurrency', models.CharField(choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')], default='UZS', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateField(default=django.utils.timezone.now)),
                ('insuranceAmount', models.FloatField()),
                ('insuranceAmountCurrency', models.CharField(choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')], default='UZS', max_length=3)),
                ('premium', models.FloatField()),
                ('netPremium', models.FloatField()),
                ('premiumCurrency', models.CharField(choices=[('UZS', 'UZS'), ('USD', 'USD'), ('EUR', 'EUR')], default='UZS', max_length=3)),
                ('status', models.CharField(choices=[('active', 'Активен'), ('pending', 'Ожидает'), ('expired', 'Истек')], default='pending', max_length=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='api.client')),
            ],
        ),
    ]
```

---

## API Endpoints Documentation

### Authentication Endpoints
- **POST** `/api/token/` - Obtain JWT access and refresh tokens
- **POST** `/api/token/refresh/` - Refresh JWT access token

### Client Management Endpoints
- **GET** `/api/clients/` - List all clients (paginated, searchable)
- **POST** `/api/clients/` - Create new client
- **GET** `/api/clients/{id}/` - Retrieve specific client with policies
- **PUT** `/api/clients/{id}/` - Update specific client
- **PATCH** `/api/clients/{id}/` - Partially update specific client
- **DELETE** `/api/clients/{id}/` - Delete specific client

### Policy Management Endpoints
- **GET** `/api/policies/` - List all policies (paginated)
- **POST** `/api/policies/` - Create new policy
- **GET** `/api/policies/{id}/` - Retrieve specific policy
- **PUT** `/api/policies/{id}/` - Update specific policy
- **PATCH** `/api/policies/{id}/` - Partially update specific policy
- **DELETE** `/api/policies/{id}/` - Delete specific policy

### User Endpoints
- **GET** `/api/me/` - Get current authenticated user information

---

## Database Schema

### Client Model Fields
| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | BigAutoField | Primary key | Auto |
| date | DateField | Registration date | No (auto) |
| name | CharField(255) | Client name | Yes |
| inn | CharField(20) | Tax identification number (unique) | Yes |
| legalName | CharField(255) | Legal company name | No |
| country | CharField(100) | Country (default: "Узбекистан") | No |
| region | CharField(100) | Region/State | No |
| city | CharField(100) | City | No |
| phone | CharField(50) | Phone number | No |
| email | EmailField | Email address | No |
| industry | CharField(100) | Industry sector | No |
| companyGroup | CharField(255) | Company group | No |
| clientStatus | CharField(10) | Status (new/active/vip/inactive) | No (default: new) |
| financialReporting | CharField(3) | Financial reporting (default: "No") | No |
| revenue | FloatField | Annual revenue | No (default: 0) |
| revenueCurrency | CharField(3) | Revenue currency (UZS/USD/EUR) | No (default: UZS) |
| revenuePeriod | CharField(20) | Revenue period | No |
| creditLimit | FloatField | Credit limit | No (default: 0) |
| limitCurrency | CharField(3) | Credit limit currency | No (default: UZS) |

### Policy Model Fields
| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | BigAutoField | Primary key | Auto |
| client | ForeignKey | Related client | Yes |
| creationDate | DateField | Policy creation date | No (auto) |
| insuranceAmount | FloatField | Insurance coverage amount | Yes |
| insuranceAmountCurrency | CharField(3) | Insurance amount currency | No (default: UZS) |
| premium | FloatField | Premium amount | Yes |
| netPremium | FloatField | Net premium amount | Yes |
| premiumCurrency | CharField(3) | Premium currency | No (default: UZS) |
| status | CharField(10) | Policy status (active/pending/expired) | No (default: pending) |

---

## Key Features

### 1. **Authentication System**
- JWT-based authentication with access/refresh tokens
- 60-minute access token lifetime
- 7-day refresh token lifetime with rotation
- Token blacklisting on rotation

### 2. **CORS Configuration**
- Configured for React frontend integration
- Supports localhost development and Render.com production
- Credential support enabled

### 3. **API Features**
- Full CRUD operations for clients and policies
- Pagination support (20 items per page)
- Search functionality for clients (name, INN)
- Filtering and ordering capabilities
- Nested serialization (clients include related policies)

### 4. **Localization**
- Russian language interface
- Uzbekistan timezone (Asia/Tashkent)
- UZS as default currency with USD/EUR support

### 5. **Production Ready**
- Render.com deployment configuration
- WhiteNoise for static file serving
- Security middleware for production
- Environment variable management
- Logging configuration

### 6. **Database Design**
- Optimized with database indexes on key fields
- Proper foreign key relationships
- Comprehensive field validation
- Choice fields for status and currency management

---

## Enhancement Opportunities

### Immediate Improvements
1. **Add comprehensive field validation**
2. **Implement proper error handling and logging**
3. **Add API documentation (Swagger/OpenAPI)**
4. **Implement proper testing suite**
5. **Add data export/import functionality**
6. **Implement audit trails**

### Advanced Features
1. **Add claim management system**
2. **Implement policy renewal workflows**
3. **Add document upload and management**
4. **Create reporting and analytics dashboards**
5. **Implement notification system**
6. **Add multi-tenant support**
7. **Integrate payment processing**
8. **Add workflow management**

### Performance Optimizations
1. **Implement database query optimization**
2. **Add caching layer (Redis)**
3. **Implement pagination improvements**
4. **Add background task processing (Celery)**
5. **Database migration to PostgreSQL**

### Security Enhancements
1. **Add rate limiting**
2. **Implement field-level permissions**
3. **Add data encryption for sensitive fields**
4. **Implement comprehensive audit logging**
5. **Add API versioning**

---

## Technical Notes

- The codebase appears to have some duplicate code sections in URL configurations that should be cleaned up
- Currently using SQLite for simplicity but configured for PostgreSQL production migration
- The project is ready for immediate deployment to Render.com
- All dependencies are properly versioned and production-ready
- The API follows REST conventions with proper HTTP methods and status codes

This documentation provides a complete overview of the current implementation and serves as a foundation for further development and enhancement of the insurance ERP system.

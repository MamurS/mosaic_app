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
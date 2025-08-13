from django.db import models

from insurance_project.apps.core.models.core import BaseModel, Country, Currency, Industry


class Entity(BaseModel):
    legal_name = models.CharField(max_length=255, db_index=True)
    registration_number = models.CharField(max_length=64, db_index=True)
    tax_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='entities')
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, related_name='entities', null=True, blank=True)

    # Address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=128, blank=True)
    region = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=32, blank=True)

    # Banking
    bank_name = models.CharField(max_length=255, blank=True)
    bank_account = models.CharField(max_length=64, blank=True)
    iban = models.CharField(max_length=34, blank=True)
    swift_bic = models.CharField(max_length=11, blank=True)

    # Compliance
    kyc_completed = models.BooleanField(default=False)
    aml_checked = models.BooleanField(default=False)
    sanctions_screened = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['registration_number']),
            models.Index(fields=['legal_name']),
            models.Index(fields=['tax_id']),
        ]
        unique_together = (
            ('legal_name', 'registration_number'),
        )

    def __str__(self) -> str:
        return f"{self.legal_name}"


class EntityRole(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]


class EntityContact(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    role = models.CharField(max_length=100, blank=True)

    class Meta:
        indexes = [models.Index(fields=['email']), models.Index(fields=['phone'])]


class EntityRelationship(BaseModel):
    from_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='relationships_from')
    to_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='relationships_to')
    relationship_type = models.CharField(max_length=100)

    class Meta:
        unique_together = (('from_entity', 'to_entity', 'relationship_type'),)


class EntityRating(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='ratings')
    rating_agency = models.CharField(max_length=100)
    rating = models.CharField(max_length=32)
    outlook = models.CharField(max_length=32, blank=True)
    effective_date = models.DateField()


class EntityFinancial(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='financials')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    period = models.CharField(max_length=16)  # e.g., '2024'
    revenue = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    ebitda = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    net_income = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        unique_together = (('entity', 'period'),)
        indexes = [models.Index(fields=['period'])]



"""
Entities domain models for MOSAIC ERP/CRM.
Covers all counterparties (corporates, individuals, gov, intermediaries) and their roles/relationships/financials.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Import shared base + user from core
from apps.core.models import BaseModel, User


class Entity(BaseModel):
    """
    Universal entity (organization / individual / government / partnership).
    A single Entity can hold multiple roles (Insured, Insurer, Reinsurer, Broker, Agent, Borrower, Lender, etc.).
    """

    class EntityType(models.TextChoices):
        CORPORATE = "CORP", "Корпоративный"
        INDIVIDUAL = "IND", "Физическое лицо"
        GOVERNMENT = "GOV", "Государственный"
        PARTNERSHIP = "PART", "Партнерство"
        FINANCIAL_INSTITUTION = "FI", "Финансовое учреждение"
        NONPROFIT = "NPO", "Некоммерческая организация"

    class RiskRating(models.TextChoices):
        AAA = "AAA", "AAA - Наивысший"
        AA_PLUS = "AA+", "AA+"
        AA = "AA", "AA"
        AA_MINUS = "AA-", "AA-"
        A_PLUS = "A+", "A+"
        A = "A", "A"
        A_MINUS = "A-", "A-"
        BBB_PLUS = "BBB+", "BBB+"
        BBB = "BBB", "BBB"
        BBB_MINUS = "BBB-", "BBB-"
        BB_PLUS = "BB+", "BB+"
        BB = "BB", "BB"
        BB_MINUS = "BB-", "BB-"
        B_PLUS = "B+", "B+"
        B = "B", "B"
        B_MINUS = "B-", "B-"
        CCC = "CCC", "CCC"
        CC = "CC", "CC"
        C = "C", "C"
        D = "D", "D - Дефолт"
        NR = "NR", "Не рейтингован"

    class EntityStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Активный"
        SUSPENDED = "SUSP", "Приостановлен"
        BLACKLISTED = "BLACK", "В черном списке"
        INACTIVE = "INACTIVE", "Неактивный"
        PENDING = "PENDING", "На рассмотрении"
        APPROVED = "APPROVED", "Одобрен"

    class ComplianceStatus(models.TextChoices):
        COMPLIANT = "COMPLIANT", "Соответствует"
        NON_COMPLIANT = "NON_COMP", "Не соответствует"
        PENDING = "PENDING", "На проверке"
        EXPIRED = "EXPIRED", "Истек"

    # Тип / регистрация
    entity_type = models.CharField(max_length=10, choices=EntityType.choices, help_text="Тип организации")
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        validators=[RegexValidator(r"^[A-Z0-9\-\/]+$", "Только A-Z, 0-9, '-', '/'")],
        help_text="ИНН/Паспорт/Регистрационный номер",
    )

    # Наименования (юрлица)
    legal_name = models.CharField(max_length=255, db_index=True, help_text="Юридическое наименование")
    legal_name_local = models.CharField(max_length=255, null=True, blank=True, help_text="На местном языке")
    trading_name = models.CharField(max_length=255, null=True, blank=True, db_index=True, help_text="Торговое наименование")
    short_name = models.CharField(max_length=100, null=True, blank=True, help_text="Краткое наименование")

    # Персональные поля (физлица)
    first_name = models.CharField(max_length=100, null=True, blank=True, help_text="Имя")
    middle_name = models.CharField(max_length=100, null=True, blank=True, help_text="Отчество")
    last_name = models.CharField(max_length=100, null=True, blank=True, help_text="Фамилия")
    date_of_birth = models.DateField(null=True, blank=True, help_text="Дата рождения")
    gender = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=[("MALE", "Мужской"), ("FEMALE", "Женский"), ("OTHER", "Другой")],
        help_text="Пол",
    )
    marital_status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[("SINGLE", "Холост/Не замужем"), ("MARRIED", "Женат/Замужем"), ("DIVORCED", "Разведен(а)"), ("WIDOWED", "Вдовец/Вдова")],
        help_text="Семейное положение",
    )

    # Регистрация/страна/отрасль
    date_of_incorporation = models.DateField(null=True, blank=True, help_text="Дата регистрации")
    country_of_incorporation = models.ForeignKey(
        "core.Country", on_delete=models.SET_NULL, null=True, blank=True, related_name="incorporated_entities", help_text="Страна регистрации"
    )
    nationality = models.ForeignKey(
        "core.Country", on_delete=models.SET_NULL, null=True, blank=True, related_name="national_entities", help_text="Национальность/Гражданство"
    )
    industry = models.ForeignKey("core.Industry", on_delete=models.SET_NULL, null=True, blank=True, help_text="Отрасль")
    occupation = models.CharField(max_length=100, null=True, blank=True, help_text="Род деятельности/Профессия")
    number_of_employees = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], help_text="Количество сотрудников")

    # Риск/кредит
    risk_rating = models.CharField(max_length=10, choices=RiskRating.choices, default=RiskRating.NR, help_text="Рейтинг риска")
    credit_limit = models.DecimalField(max_digits=20, decimal_places=2, default=0, validators=[MinValueValidator(0)], help_text="Кредитный лимит")
    credit_limit_currency = models.ForeignKey(
        "core.Currency", on_delete=models.SET_NULL, null=True, blank=True, related_name="entity_credit_limits", help_text="Валюта кредитного лимита"
    )
    credit_terms_days = models.IntegerField(default=30, validators=[MinValueValidator(0), MaxValueValidator(365)], help_text="Отсрочка (дни)")

    # Комплаенс/статусы
    entity_status = models.CharField(max_length=10, choices=EntityStatus.choices, default=EntityStatus.PENDING, help_text="Статус организации")
    kyc_status = models.CharField(max_length=20, choices=ComplianceStatus.choices, default=ComplianceStatus.PENDING, help_text="Статус KYC")
    kyc_date = models.DateField(null=True, blank=True, help_text="Дата проверки KYC")
    kyc_expiry_date = models.DateField(null=True, blank=True, help_text="KYC истекает")
    aml_status = models.CharField(max_length=20, choices=ComplianceStatus.choices, default=ComplianceStatus.PENDING, help_text="Статус AML")
    aml_date = models.DateField(null=True, blank=True, help_text="Дата AML-проверки")
    sanction_check_status = models.CharField(max_length=20, choices=ComplianceStatus.choices, default=ComplianceStatus.PENDING, help_text="Статус санкц. проверки")
    sanction_check_date = models.DateField(null=True, blank=True, help_text="Дата санкц. проверки")
    compliance_notes = models.TextField(null=True, blank=True, help_text="Примечания по соответствию")

    # Иерархия
    parent_entity = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subsidiaries", help_text="Родительская организация")
    ultimate_parent_entity = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="ultimate_subsidiaries", help_text="Конечная материнская")

    # Контакты (общие)
    email = models.EmailField(null=True, blank=True, help_text="Основной email")
    secondary_email = models.EmailField(null=True, blank=True, help_text="Доп. email")
    phone = models.CharField(max_length=50, null=True, blank=True, help_text="Телефон")
    mobile = models.CharField(max_length=50, null=True, blank=True, help_text="Мобильный")
    fax = models.CharField(max_length=50, null=True, blank=True, help_text="Факс")
    website = models.URLField(null=True, blank=True, help_text="Веб-сайт")

    # Адрес
    address_line1 = models.CharField(max_length=255, null=True, blank=True, help_text="Адрес строка 1")
    address_line2 = models.CharField(max_length=255, null=True, blank=True, help_text="Адрес строка 2")
    city = models.CharField(max_length=100, null=True, blank=True, help_text="Город")
    state_province = models.CharField(max_length=100, null=True, blank=True, help_text="Область/Регион")
    postal_code = models.CharField(max_length=20, null=True, blank=True, help_text="Индекс")
    country = models.ForeignKey("core.Country", on_delete=models.SET_NULL, null=True, blank=True, related_name="entities", help_text="Страна")

    # Почтовый адрес
    mailing_same_as_physical = models.BooleanField(default=True, help_text="Почтовый адрес совпадает")
    mailing_address_line1 = models.CharField(max_length=255, null=True, blank=True, help_text="Почтовый адрес 1")
    mailing_address_line2 = models.CharField(max_length=255, null=True, blank=True, help_text="Почтовый адрес 2")
    mailing_city = models.CharField(max_length=100, null=True, blank=True, help_text="Почтовый город")
    mailing_state_province = models.CharField(max_length=100, null=True, blank=True, help_text="Почтовая область/регион")
    mailing_postal_code = models.CharField(max_length=20, null=True, blank=True, help_text="Почтовый индекс")
    mailing_country = models.ForeignKey("core.Country", on_delete=models.SET_NULL, null=True, blank=True, related_name="mailing_entities", help_text="Почтовая страна")

    # Финансы (высокоуровневые)
    annual_revenue = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)], help_text="Годовой доход")
    revenue_currency = models.ForeignKey("core.Currency", on_delete=models.SET_NULL, null=True, blank=True, related_name="entity_revenues", help_text="Валюта дохода")
    revenue_year = models.IntegerField(null=True, blank=True, help_text="Год дохода")
    net_worth = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Чистая стоимость")
    total_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)], help_text="Всего активов")

    # Налоги/банки
    tax_id = models.CharField(max_length=50, null=True, blank=True, help_text="Налоговый номер")
    vat_number = models.CharField(max_length=50, null=True, blank=True, help_text="НДС номер")
    tax_residence = models.ForeignKey("core.Country", on_delete=models.SET_NULL, null=True, blank=True, related_name="tax_resident_entities", help_text="Налоговое резидентство")

    bank_name = models.CharField(max_length=255, null=True, blank=True, help_text="Банк")
    bank_account_number = models.CharField(max_length=50, null=True, blank=True, help_text="№ счета")
    bank_swift_code = models.CharField(max_length=20, null=True, blank=True, help_text="SWIFT")
    bank_iban = models.CharField(max_length=50, null=True, blank=True, help_text="IBAN")

    # Предпочтения
    preferred_language = models.CharField(max_length=10, default="ru", choices=[("ru", "Русский"), ("en", "English"), ("uz", "O'zbek")], help_text="Язык")
    preferred_communication = models.CharField(
        max_length=20,
        default="EMAIL",
        choices=[("EMAIL", "Email"), ("PHONE", "Телефон"), ("SMS", "SMS"), ("MAIL", "Почта"), ("WHATSAPP", "WhatsApp"), ("TELEGRAM", "Telegram")],
        help_text="Канал связи",
    )

    # Прочее
    notes = models.TextField(null=True, blank=True, help_text="Примечания")
    tags = models.JSONField(default=list, blank=True, help_text="Теги")
    custom_fields = models.JSONField(default=dict, blank=True, help_text="Пользовательские поля")

    class Meta:
        db_table = "entities"
        verbose_name = "Entity"
        verbose_name_plural = "Entities"
        indexes = [
            models.Index(fields=["entity_type", "entity_status"]),
            models.Index(fields=["risk_rating"]),
            models.Index(fields=["legal_name"]),
            models.Index(fields=["trading_name"]),
            models.Index(fields=["registration_number"]),
            models.Index(fields=["kyc_status", "aml_status"]),
        ]
        ordering = ["legal_name"]

    def __str__(self):
        if self.entity_type == self.EntityType.INDIVIDUAL:
            return f"{(self.last_name or '').strip()} {(self.first_name or '').strip()} ({self.registration_number})".strip()
        return f"{self.legal_name} ({self.registration_number})"

    @property
    def display_name(self):
        if self.entity_type == self.EntityType.INDIVIDUAL:
            return f"{(self.first_name or '').strip()} {(self.last_name or '').strip()}".strip() or self.registration_number
        return self.trading_name or self.short_name or self.legal_name

    @property
    def is_compliant(self) -> bool:
        return all(
            [
                self.kyc_status == self.ComplianceStatus.COMPLIANT,
                self.aml_status == self.ComplianceStatus.COMPLIANT,
                self.sanction_check_status == self.ComplianceStatus.COMPLIANT,
            ]
        )


class EntityRole(BaseModel):
    """Roles a given Entity can play (multiple allowed)."""

    class RoleType(models.TextChoices):
        # Primary insurance
        INSURER = "INSURER", "Страховщик"
        INSURED = "INSURED", "Страхователь"
        POLICYHOLDER = "HOLDER", "Держатель полиса"
        BENEFICIARY = "BENEF", "Выгодоприобретатель"
        # Reinsurance
        REINSURER = "REINSURER", "Перестраховщик"
        CEDENT = "CEDENT", "Цедент"
        RETROCEDENT = "RETRO", "Ретроцедент"
        RETROCESSIONAIRE = "RETROCESS", "Ретроцессионер"
        # Intermediaries
        BROKER = "BROKER", "Брокер"
        AGENT = "AGENT", "Агент"
        UNDERWRITING_AGENT = "UW_AGENT", "Андеррайтинг-агент"
        MANAGING_AGENT = "MGA", "Управляющий агент"
        # Credit insurance
        BORROWER = "BORROWER", "Заемщик"
        LENDER = "LENDER", "Кредитор"
        GUARANTOR = "GUARANTOR", "Гарант"
        # Service Providers
        SURVEYOR = "SURVEYOR", "Сюрвейер"
        LOSS_ADJUSTER = "ADJUSTER", "Аджастер"
        ACTUARY = "ACTUARY", "Актуарий"
        AUDITOR = "AUDITOR", "Аудитор"
        LAWYER = "LAWYER", "Юрист"
        # Other
        VENDOR = "VENDOR", "Поставщик"
        PARTNER = "PARTNER", "Партнер"
        REGULATOR = "REGULATOR", "Регулятор"

    class RoleStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Активный"
        INACTIVE = "INACTIVE", "Неактивный"
        SUSPENDED = "SUSPENDED", "Приостановлен"
        EXPIRED = "EXPIRED", "Истек"
        PENDING = "PENDING", "На рассмотрении"

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="roles", help_text="Организация")
    role_type = models.CharField(max_length=20, choices=RoleType.choices, help_text="Тип роли")
    role_status = models.CharField(max_length=20, choices=RoleStatus.choices, default=RoleStatus.PENDING, help_text="Статус роли")

    effective_date = models.DateField(default=timezone.now, help_text="Начало")
    expiry_date = models.DateField(null=True, blank=True, help_text="Окончание")

    # Licensing (for regulated roles)
    license_number = models.CharField(max_length=50, null=True, blank=True, help_text="Номер лицензии")
    license_issue_date = models.DateField(null=True, blank=True, help_text="Дата выдачи")
    license_expiry_date = models.DateField(null=True, blank=True, help_text="Действует до")
    license_issuer = models.CharField(max_length=255, null=True, blank=True, help_text="Кем выдано")

    # Territory/jurisdiction
    territory = models.CharField(max_length=255, null=True, blank=True, help_text="Территория")
    jurisdiction = models.CharField(max_length=255, null=True, blank=True, help_text="Юрисдикция")

    # Authority limits
    authority_limits = models.JSONField(default=dict, blank=True, help_text="Лимиты полномочий (JSON)")
    underwriting_limit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Лимит андеррайтинга")
    claim_settlement_limit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Лимит урегулирования")

    # Intermediary commission
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Комиссия %"
    )
    commission_structure = models.JSONField(default=dict, blank=True, help_text="Структура комиссии (JSON)")

    # Approval
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_entity_roles", help_text="Кем одобрено")
    approval_date = models.DateTimeField(null=True, blank=True, help_text="Дата одобрения")
    approval_notes = models.TextField(null=True, blank=True, help_text="Примечания")

    notes = models.TextField(null=True, blank=True, help_text="Примечания")

    class Meta:
        db_table = "entity_roles"
        verbose_name = "Entity Role"
        verbose_name_plural = "Entity Roles"
        unique_together = [("entity", "role_type", "effective_date")]
        indexes = [
            models.Index(fields=["role_type", "role_status"]),
            models.Index(fields=["effective_date", "expiry_date"]),
        ]
        ordering = ["-effective_date"]

    def __str__(self):
        return f"{self.entity.display_name} - {self.get_role_type_display()}"

    @property
    def is_valid(self) -> bool:
        today = timezone.now().date()
        return (
            self.role_status == self.RoleStatus.ACTIVE
            and self.effective_date <= today
            and (self.expiry_date is None or self.expiry_date >= today)
        )


class EntityContact(BaseModel):
    """Named contact persons for an Entity."""

    class ContactType(models.TextChoices):
        PRIMARY = "PRIMARY", "Основной"
        BILLING = "BILLING", "По счетам"
        TECHNICAL = "TECH", "Технический"
        CLAIMS = "CLAIMS", "По убыткам"
        UNDERWRITING = "UW", "По андеррайтингу"
        MANAGEMENT = "MGMT", "Руководство"
        OTHER = "OTHER", "Другой"

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="contacts", help_text="Организация")
    contact_type = models.CharField(max_length=20, choices=ContactType.choices, default=ContactType.PRIMARY, help_text="Тип контакта")

    salutation = models.CharField(max_length=20, null=True, blank=True, choices=[("MR", "Г-н"), ("MRS", "Г-жа"), ("MS", "Г-жа"), ("DR", "Д-р"), ("PROF", "Проф.")], help_text="Обращение")
    first_name = models.CharField(max_length=100, help_text="Имя")
    last_name = models.CharField(max_length=100, help_text="Фамилия")
    middle_name = models.CharField(max_length=100, null=True, blank=True, help_text="Отчество")

    job_title = models.CharField(max_length=100, null=True, blank=True, help_text="Должность")
    department = models.CharField(max_length=100, null=True, blank=True, help_text="Отдел")

    email = models.EmailField(help_text="Email")
    phone = models.CharField(max_length=50, null=True, blank=True, help_text="Телефон")
    mobile = models.CharField(max_length=50, null=True, blank=True, help_text="Мобильный")
    fax = models.CharField(max_length=50, null=True, blank=True, help_text="Факс")

    preferred_language = models.CharField(max_length=10, default="ru", choices=[("ru", "Русский"), ("en", "English"), ("uz", "O'zbek")], help_text="Язык")
    preferred_contact_method = models.CharField(
        max_length=20,
        default="EMAIL",
        choices=[("EMAIL", "Email"), ("PHONE", "Телефон"), ("SMS", "SMS"), ("WHATSAPP", "WhatsApp"), ("TELEGRAM", "Telegram")],
        help_text="Канал связи",
    )

    available_from = models.TimeField(null=True, blank=True, help_text="Доступен с")
    available_to = models.TimeField(null=True, blank=True, help_text="Доступен до")
    time_zone = models.CharField(max_length=50, default="Asia/Tashkent", help_text="Часовой пояс")

    is_primary = models.BooleanField(default=False, help_text="Основной контакт")
    is_active = models.BooleanField(default=True, help_text="Активен")
    notes = models.TextField(null=True, blank=True, help_text="Примечания")

    class Meta:
        db_table = "entity_contacts"
        verbose_name = "Entity Contact"
        verbose_name_plural = "Entity Contacts"
        indexes = [models.Index(fields=["entity", "contact_type"]), models.Index(fields=["is_primary", "is_active"])]
        ordering = ["-is_primary", "contact_type", "last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.entity.display_name}".strip()

    @property
    def full_name(self) -> str:
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join([p for p in parts if p])


class EntityRelationship(BaseModel):
    """Relationships between entities (parent/subsidiary, broker↔client, reinsurer↔cedent, etc.)."""

    class RelationshipType(models.TextChoices):
        PARENT_SUBSIDIARY = "PARENT_SUB", "Материнская-Дочерняя"
        SISTER_COMPANY = "SISTER", "Сестринские компании"
        JOINT_VENTURE = "JV", "Совместное предприятие"
        PARTNERSHIP = "PARTNER", "Партнерство"
        CONSORTIUM = "CONSORT", "Консорциум"
        FRANCHISE = "FRANCHISE", "Франшиза"
        AGENT_PRINCIPAL = "AGENT_PRIN", "Агент-Принципал"
        BROKER_CLIENT = "BROKER_CLI", "Брокер-Клиент"
        REINSURER_CEDENT = "RI_CEDENT", "Перестраховщик-Цедент"
        OTHER = "OTHER", "Другое"

    entity_from = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="relationships_from", help_text="Организация (от)")
    entity_to = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="relationships_to", help_text="Организация (к)")

    relationship_type = models.CharField(max_length=20, choices=RelationshipType.choices, help_text="Тип отношений")
    ownership_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Доля владения %"
    )

    effective_date = models.DateField(default=timezone.now, help_text="Начало")
    expiry_date = models.DateField(null=True, blank=True, help_text="Окончание")

    is_active = models.BooleanField(default=True, help_text="Активно")
    description = models.TextField(null=True, blank=True, help_text="Описание")
    agreement_reference = models.CharField(max_length=100, null=True, blank=True, help_text="Ссылка на соглашение")

    class Meta:
        db_table = "entity_relationships"
        verbose_name = "Entity Relationship"
        verbose_name_plural = "Entity Relationships"
        unique_together = [("entity_from", "entity_to", "relationship_type", "effective_date")]
        indexes = [
            models.Index(fields=["relationship_type", "is_active"]),
            models.Index(fields=["effective_date", "expiry_date"]),
        ]

    def __str__(self):
        return f"{self.entity_from.display_name} - {self.get_relationship_type_display()} - {self.entity_to.display_name}"


class EntityRating(BaseModel):
    """Rating history for an entity (external & internal)."""

    class RatingAgency(models.TextChoices):
        MOODYS = "MOODYS", "Moody's"
        SP = "SP", "S&P"
        FITCH = "FITCH", "Fitch"
        AM_BEST = "AMBEST", "A.M. Best"
        LOCAL = "LOCAL", "Местное агентство"
        INTERNAL = "INTERNAL", "Внутренний рейтинг"
        OTHER = "OTHER", "Другое"

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="ratings", help_text="Организация")
    rating_agency = models.CharField(max_length=20, choices=RatingAgency.choices, help_text="Агентство")
    rating = models.CharField(max_length=10, help_text="Рейтинг")
    rating_outlook = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[("POSITIVE", "Позитивный"), ("STABLE", "Стабильный"), ("NEGATIVE", "Негативный"), ("DEVELOPING", "Развивающийся")],
        help_text="Прогноз",
    )

    rating_date = models.DateField(help_text="Дата рейтинга")
    valid_until = models.DateField(null=True, blank=True, help_text="Действителен до")

    financial_strength_rating = models.CharField(max_length=10, null=True, blank=True, help_text="FSR (для страховщиков)")
    report_url = models.URLField(null=True, blank=True, help_text="Ссылка на отчет")
    notes = models.TextField(null=True, blank=True, help_text="Примечания")

    class Meta:
        db_table = "entity_ratings"
        verbose_name = "Entity Rating"
        verbose_name_plural = "Entity Ratings"
        indexes = [models.Index(fields=["entity", "rating_date"]), models.Index(fields=["rating_agency", "rating"])]
        ordering = ["-rating_date"]

    def __str__(self):
        return f"{self.entity.display_name} - {self.rating} ({self.rating_agency})"


class EntityFinancial(BaseModel):
    """Financial statements & ratios per entity (annual/periodic)."""

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="financials", help_text="Организация")

    financial_year = models.IntegerField(help_text="Финансовый год")
    period_start = models.DateField(help_text="Начало периода")
    period_end = models.DateField(help_text="Конец периода")
    is_audited = models.BooleanField(default=False, help_text="Аудировано")

    # P&L
    revenue = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Выручка")
    gross_profit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Валовая прибыль")
    operating_profit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Опер. прибыль")
    net_profit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Чистая прибыль")
    ebitda = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="EBITDA")

    # Balance sheet
    total_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Всего активов")
    current_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Оборотные активы")
    fixed_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Основные средства")
    total_liabilities = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Всего обязательств")
    current_liabilities = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Краткосрочные обязательства")
    long_term_debt = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Долгосрочный долг")
    equity = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Собственный капитал")

    # Ratios
    current_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Текущая ликвидность")
    quick_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Быстрая ликвидность")
    debt_to_equity_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Debt/Equity")
    return_on_assets = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="ROA")
    return_on_equity = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="ROE")
    profit_margin = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Маржа прибыли")

    # Insurance KPIs
    gross_written_premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="GWP")
    net_written_premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="NWP")
    loss_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Loss Ratio")
    expense_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Expense Ratio")
    combined_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Combined Ratio")
    solvency_ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Solvency Ratio")

    currency = models.ForeignKey("core.Currency", on_delete=models.SET_NULL, null=True, help_text="Валюта")
    auditor = models.CharField(max_length=255, null=True, blank=True, help_text="Аудитор")
    audit_opinion = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=[("UNQUALIFIED", "Безоговорочное"), ("QUALIFIED", "С оговорками"), ("ADVERSE", "Отрицательное"), ("DISCLAIMER", "Отказ от мнения")],
        help_text="Аудиторское заключение",
    )

    financial_statement_url = models.URLField(null=True, blank=True, help_text="Ссылка на фин. отчет")
    notes = models.TextField(null=True, blank=True, help_text="Примечания")

    class Meta:
        db_table = "entity_financials"
        verbose_name = "Entity Financial"
        verbose_name_plural = "Entity Financials"
        unique_together = [("entity", "financial_year", "period_end")]
        indexes = [models.Index(fields=["entity", "financial_year"]), models.Index(fields=["is_audited"])]
        ordering = ["-financial_year", "-period_end"]

    def __str__(self):
        return f"{self.entity.display_name} - {self.financial_year}"

    def calculate_ratios(self):
        """Helper to compute common ratios from available fields."""
        if self.current_assets and self.current_liabilities and self.current_liabilities > 0:
            self.current_ratio = self.current_assets / self.current_liabilities
        if self.total_liabilities and self.equity and self.equity > 0:
            self.debt_to_equity_ratio = self.total_liabilities / self.equity
        if self.net_profit and self.total_assets and self.total_assets > 0:
            self.return_on_assets = self.net_profit / self.total_assets
        if self.net_profit and self.equity and self.equity > 0:
            self.return_on_equity = self.net_profit / self.equity
        if self.net_profit and self.revenue and self.revenue > 0:
            self.profit_margin = self.net_profit / self.revenue
        if self.loss_ratio is not None and self.expense_ratio is not None:
            self.combined_ratio = self.loss_ratio + self.expense_ratio

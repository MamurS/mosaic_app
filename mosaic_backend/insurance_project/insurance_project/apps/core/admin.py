from django.contrib import admin

from .models import AuditLog, Country, Currency, Industry, SystemSetting


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('is_active',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('is_active',)


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'is_active')
    search_fields = ('key',)
    list_filter = ('is_active',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'actor', 'created_at')
    readonly_fields = ('id', 'event_type', 'actor', 'created_at', 'payload')
    search_fields = ('event_type', 'actor__email')
    list_filter = ('event_type',)



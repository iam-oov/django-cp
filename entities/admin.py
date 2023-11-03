from django.contrib import admin
from .models import Entity, FederalEntity, Municipality, Settlement


class MunicipalityInline(admin.TabularInline):
    model = Municipality
    extra = 1


class SettlementInline(admin.TabularInline):
    model = Settlement
    extra = 1


class EntityInline(admin.TabularInline):
    model = Entity
    extra = 1


class FederalEntityAdmin(admin.ModelAdmin):
    list_display = ['slug', 'key', 'name', 'code']
    prepopulated_fields = {'slug': ['name']}
    inlines = [MunicipalityInline]


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ['slug', 'key', 'name', 'federal_entity']
    prepopulated_fields = {'slug': ['name']}
    inlines = [SettlementInline]


class SettlementAdmin(admin.ModelAdmin):
    list_display = ['slug', 'key', 'name', 'zone_type', 'type', 'municipality']
    prepopulated_fields = {'slug': ['name']}
    inlines = [EntityInline]


class EntityAdmin(admin.ModelAdmin):
    list_display = ['zip_code', 'locality', 'slug', 'settlement']
    search_fields = ['zip_code']
    prepopulated_fields = {'slug': ['locality']}


admin.site.register(Entity, EntityAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(FederalEntity, FederalEntityAdmin)
admin.site.register(Settlement, SettlementAdmin)

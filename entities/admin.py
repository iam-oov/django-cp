from django.contrib import admin
from .models import Entity, FederalEntity, Municipality, Settlement


class EntityInline(admin.TabularInline):
    model = Entity
    extra = 1


class FederalEntityInline(admin.TabularInline):
    model = FederalEntity
    extra = 1


class MunicipalityInline(admin.TabularInline):
    model = Municipality
    extra = 1


class EntityAdmin(admin.ModelAdmin):
    list_display = ['zip_code', 'locality', 'slug']
    prepopulated_fields = {'slug': ['locality']}


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ['slug', 'key', 'name', 'settlement']
    prepopulated_fields = {'slug': ['name']}
    inlines = [FederalEntityInline]


class FederalEntityAdmin(admin.ModelAdmin):
    list_display = ['slug', 'key', 'name', 'code', 'municipality']
    prepopulated_fields = {'slug': ['name']}
    inlines = [EntityInline]


class SettlementAdmin(admin.ModelAdmin):
    list_display = ['slug', 'key', 'name', 'zone_type', 'type']
    prepopulated_fields = {'slug': ['name']}
    inlines = [MunicipalityInline]


admin.site.register(Entity, EntityAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(FederalEntity, FederalEntityAdmin)
admin.site.register(Settlement, SettlementAdmin)

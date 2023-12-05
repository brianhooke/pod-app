from django.contrib import admin
from .models import Material
from .models import Supplier

class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id","material", "units", "rate", "supplier")
    ordering=('id',)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id","supplier", "contact", "email", "phone")
    ordering=('id',)

admin.site.register(Material, MaterialAdmin)
admin.site.register(Supplier, SupplierAdmin)
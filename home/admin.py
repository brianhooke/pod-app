from django.contrib import admin
from .models import Material
from .models import Supplier
from .models import BomMaterial
from .models import BomProduct

class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id","material", "units", "rate", "supplier")
    ordering=('id',)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id","supplier", "contact", "email", "phone")
    ordering=('id',)

class BomMaterialAdmin(admin.ModelAdmin):
    list_display = ("id","product","material", "quantity")
    ordering=('id',)

class BomProductAdmin(admin.ModelAdmin):
    list_display = ("id","product_name")
    ordering=('id',)

admin.site.register(Material, MaterialAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(BomMaterial, BomMaterialAdmin)
admin.site.register(BomProduct, BomProductAdmin)
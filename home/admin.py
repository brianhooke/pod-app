from django.contrib import admin
from .models import Material

class MaterialAdmin(admin.ModelAdmin):
    list_display = ("material", "units", "rate", "supplier")

admin.site.register(Material, MaterialAdmin)
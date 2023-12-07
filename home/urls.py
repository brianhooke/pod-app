from django.urls import path
from . import views
from .views import supplier_view
from .views import save_supplier
from .views import update_supplier
from .views import delete_supplier
from .views import save_material_rate
from .views import update_material_rate
from .views import delete_material_rate
from .views import bom_view


urlpatterns = [
    path('', views.main, name='main'),
    path('master_rates/', views.master_rates, name='master_rates'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('testing/', views.testing, name='testing'),
    path('save_supplier/', save_supplier, name='save_supplier'),
    path('update_supplier/', update_supplier, name='update_supplier'),
    path('delete_supplier/', views.delete_supplier, name='delete_supplier'),
    path('update_material_rate/', views.update_material_rate, name='update_material_rate'),
    path('delete_material_rate/', views.delete_material_rate, name='delete_material_rate'),
    path('save_material_rate/', views.save_material_rate, name='save_material_rate'),   
    path('bom/', bom_view, name='bom'),
    path('supplier/', supplier_view, name='supplier-form')
]
from django.urls import path
from . import views
from .views import supplier_view
from .views import save_supplier
from .views import update_supplier

urlpatterns = [
    path('', views.main, name='main'),
    path('master_rates/', views.master_rates, name='master_rates'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('testing/', views.testing, name='testing'),
    path('save_supplier/', save_supplier, name='save_supplier'),
    path('update_supplier/', update_supplier, name='update_supplier'),
    path('supplier/', supplier_view, name='supplier-form')
]
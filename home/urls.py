from django.urls import path
from . import views
from .views import supplier_view

urlpatterns = [
    path('', views.main, name='main'),
    path('master_rates/', views.master_rates, name='master_rates'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('testing/', views.testing, name='testing'),
    path('supplier/', supplier_view, name='supplier-form')
]
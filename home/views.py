from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Material
from .models import Supplier
from .forms import SupplierForm
import json

def main(request):
    template = loader.get_template('main.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def master_rates(request):
    materials_list= Material.objects.all().values()
    template = loader.get_template('master_rates.html')
    context = {
       'materials_list': materials_list,
    }
    return HttpResponse(template.render(context, request))

def suppliers(request):
    suppliers_list= Supplier.objects.all().values()
    template = loader.get_template('suppliers.html')
    context = {
       'suppliers_list': suppliers_list,
    }
    return HttpResponse(template.render(context, request))

def testing(request):
    template = loader.get_template('template.html')
    context = {
        'fruits': ['Apple', 'Banana', 'Cheery']
    }
    return HttpResponse(template.render(context, request))

def supplier_view(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suppliers.html')  # Replace with your success URL
    else:
        form = SupplierForm()

    return render(request, 'suppliers.html', {'form': form})

# require_POST
# csrf_exempt
def save_supplier(request):
    try:
        data = json.loads(request.body)
        supplier = Supplier(
            supplier=data['supplier'],
            contact=data['contact'],
            email=data['email'],
            phone=data['phone']
        )
        supplier.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def update_supplier(request):
    try:
        data = json.loads(request.body)
        supplier_obj = Supplier.objects.get(id=data['id'])
        # Assume 'supplier' is unique for simplicity. In practice, use a unique identifier like an ID.
        supplier_obj = Supplier.objects.get(supplier=data['supplier'])
        supplier_obj.contact = data['contact']
        supplier_obj.email = data['email']
        supplier_obj.phone = data['phone']
        supplier_obj.save()
        return JsonResponse({'status': 'success'})
    except Supplier.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Supplier not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
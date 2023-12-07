from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Material
from .models import Supplier
from .models import BomProduct
from .models import BomMaterial
from .forms import SupplierForm
import json

def main(request):
    template = loader.get_template('main.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def master_rates(request):
    materials_list= Material.objects.all().values()
    suppliers_list=Supplier.objects.all().values('id', 'supplier')
    template = loader.get_template('master_rates.html')
    context = {
       'materials_list': materials_list,
       'suppliers_list': suppliers_list,
    }
    return HttpResponse(template.render(context, request))

def suppliers(request):
    suppliers_list= Supplier.objects.all().values()
    template = loader.get_template('suppliers.html')
    context = {
       'suppliers_list': suppliers_list,
    }
    return HttpResponse(template.render(context, request))

def bom_view(request):
    products = BomProduct.objects.all()
    return render(request, 'bom.html', {'products': products})

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
        # Fetch the supplier object based on the ID
        supplier_obj = Supplier.objects.get(id=data['id'])
        # Update the fields
        supplier_obj.supplier = data['supplier']
        supplier_obj.contact = data['contact']
        supplier_obj.email = data['email']
        supplier_obj.phone = data['phone']
        supplier_obj.save()
        return JsonResponse({'status': 'success'})
    except Supplier.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Supplier not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def delete_supplier(request):
    try:
        data = json.loads(request.body)
        supplier_obj = Supplier.objects.get(id=data['id'])
        supplier_obj.delete()
        return JsonResponse({'status': 'success'})
    except Supplier.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Supplier not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@require_POST
def update_material_rate(request):
    try:
        data = json.loads(request.body)
        material = Material.objects.get(pk=data['id'])
        material.material = data['material']
        material.units = data['units']
        material.rate = data['rate']

        # Assuming `supplier` in Material is a CharField and stores the name
        material.supplier = data['supplier']  # Directly using the supplier's name

        material.save()
        return JsonResponse({'status': 'success', 'message': 'Material rate updated successfully.'})
    except Material.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Material not found.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@require_POST
def delete_material_rate(request):
    try:
        data = json.loads(request.body)
        material_id = data.get('id')
        material = Material.objects.get(pk=material_id)
        material.delete()
        return JsonResponse({'status': 'success', 'message': 'Material rate deleted successfully.'})
    except Material.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Material not found.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_POST
def save_material_rate(request):
    try:
        data = json.loads(request.body)
        # Create a new Material object
        new_material = Material(
            material=data['material'],
            units=data['units'],
            rate=data['rate'],
            supplier=data['supplier']
        )
        new_material.save()
        return JsonResponse({'status': 'success', 'message': 'Material rate saved successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def bom_view(request):
    products = BomProduct.objects.all()
    product_materials = []

    for product in products:
        # Replace the following line with your logic to get materials for a product
        materials = Material.objects.all()  # Assuming you want to show all materials for now
        product_materials.append((product, materials))

    return render(request, 'bom.html', {'product_materials': product_materials})

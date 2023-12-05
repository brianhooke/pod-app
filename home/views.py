from django.http import HttpResponse
from django.template import loader
from .models import Material
from .models import Supplier
from .forms import SupplierForm

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
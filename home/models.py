from django.db import models

class Material(models.Model):
    material = models.CharField(max_length=255)
    units=models.CharField(max_length=255)
    rate= models.DecimalField(max_digits=8, decimal_places=2)
    supplier= models.CharField(max_length=255) # remember supplier will be linked from a dropdown in future

    def __str__(self):
        return f"{self.material} {self.units} {self.rate} {self.supplier}"
    

class Supplier(models.Model):
    supplier = models.CharField(max_length=255)
    contact=models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    phone= models.CharField(max_length=255)

    def __str__(self):
        return f"{self.supplier} {self.contact} {self.email} {self.phone}"
# Create your models here.

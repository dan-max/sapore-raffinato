from time import timezone
from django.db import models
from django.contrib.auth.models import User
class Task(models.Model):
    title= models.CharField(max_length=100)
    description= models.TextField(blank=True)
    created= models.DateTimeField(auto_now_add=True)
    datecompleted= models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='upload', null=True)
    precio=models.DecimalField(max_digits=18, decimal_places=2, null=True)
    def __str__(self):
        return f"{self.title} - by {self.user.username}"

class Consumo(models.Model):
    producto=models.ForeignKey(Task,on_delete=models.CASCADE)
    cantidad=models.PositiveIntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    dateConsumption=models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"{self.producto}  {self.cantidad} unidades"
    
class ModeloVacio(models.Model):
    pass
class Sell(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    totalSell=models.DecimalField(max_digits=18, decimal_places=2, null=True)
    dateSell= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} compro {self.totalSell} el  {self.dateSell} "
class Sellsaved(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    dateSellSaved= models.DateTimeField(auto_now_add=True)
    consumption=  models.PositiveIntegerField(default=1)
    totalConsumption= models.DecimalField(max_digits=18, decimal_places=2, null=True)
    cantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.user} consumio esto {self.consumption} y costo  {self.totalConsumption} "
from django.forms import ModelForm
from .models  import Task, Consumo, ModeloVacio, Sell
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model= Task
        fields= ['title', 'description','image','precio']
        

class Cobro(ModelForm):
    class Meta:
        model= Consumo
        fields= ['producto', 'cantidad']       

class FormularioContacto(forms.ModelForm):
    class Meta:
        model = ModeloVacio
        fields = []
        
class finishSell(ModelForm):
    class Meta:
        model = Sell
        fields = ['totalSell']
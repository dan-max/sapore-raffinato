import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, request, JsonResponse
from django.contrib.auth import login, logout, authenticate
from .form import TaskForm
from .models import Task, Consumo, ModeloVacio, Sell, Sellsaved
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models

def helloworld(request, task_id=None):
    tasks = Task.objects.filter(datecompleted__isnull=True)
    task2 = Consumo.objects.all()
    consumo_obj = get_object_or_404(Consumo, producto__id=task_id) if task_id else None
    user = request.user
    
    if request.method == 'GET':
        
        return render(request, 'home.html', {'tasks': tasks, 'task2': task2})
    elif request.method == 'POST':
        if 'task_id' in request.POST:
            task_id = request.POST['task_id']
            product = get_object_or_404(Task, pk=task_id)
            consumo_obj, created = Consumo.objects.get_or_create(producto=product,user=user, defaults={'cantidad': 0})
            
            # Incrementar el valor de cant
            consumo_obj.cantidad += 1
            consumo_obj.save()
            print("conseguido")
            return JsonResponse({'message': 'Success'})
    else:
        return render(request, 'home.html')
    
    # Resto de tu código
    return render(request, 'home.html', {'tasks': tasks, 'task2': task2})

def singup(request):
    if request.method== 'GET':
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user= User.objects.create_user(username=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect("home")
            except:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'username already exist'
                })
        return render(request, 'singup.html',{
            'form': UserCreationForm,
            'error': 'password do not match'
        })

@login_required

def singout(request):
    logout(request)
    return redirect('home')

def singin(request):

    if request.method == "GET":

        return render(request, 'singin.html', {
            'form': AuthenticationForm
        })
    else:
        user=authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'singin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('home')

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    usuario_actual = request.user
    consumos = Consumo.objects.filter(user=usuario_actual)
    tareas = Task.objects.filter(id__in=[consumo.producto.id for consumo in consumos])
    # Crear un diccionario que mapea id de tarea a precio
    id_to_precio = {tarea.id: tarea.precio for tarea in tareas}
    print(task)
    if request.method == 'POST':
        pass
        
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_detail.html', {'task': task, 'form': form, 'consumos':consumos, 'tareas':tareas})

@login_required
def carrito(request):
    usuario_actual = request.user
    consumos = Consumo.objects.filter(user=usuario_actual).values('producto', 'cantidad')
    tareas = Task.objects.filter(id__in=[consumo['producto'] for consumo in consumos]).values('id', 'title', 'precio')
    # Crear un diccionario que mapea id de tarea a título y precio
    id_to_info = {tarea['id']: {'title': tarea['title'], 'precio': tarea['precio']} for tarea in tareas}
    
    # Completar la información de consumos con títulos y precios
    for consumo in consumos:
        info_tarea = id_to_info.get(consumo['producto'])
        if info_tarea:
            consumo['title'] = info_tarea['title']
            consumo['precio'] = info_tarea['precio']
        else:
            consumo['title'] = 'Sin título'
            consumo['precio'] = None

    if request.method == 'GET':
        return render(request, 'carrito.html', {'consumos': consumos, 'tareas': tareas})
    elif request.method == 'POST':

        try:
        # Acceder a los datos de un formulario codificado como 'application/x-www-form-urlencoded'
            total = request.POST.get('total')
            sell = Sell(totalSell=total, user=usuario_actual)
            sell.save()
            print("guardado correctamente")
            print(total)
        
        # Enviar una respuesta JSON en lugar de redireccionar
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return render(request, 'carrito.html')

def finish_Sell(request):
    lastSell = Sell.objects.last()
    usuario_actual = request.user
    consumos = Consumo.objects.filter(user=usuario_actual)
    if request.method == 'GET':
        tareas = Task.objects.filter(id__in=[consumo.producto.id for consumo in consumos])

        # Crear un diccionario que mapea id de tarea a precio
        id_to_precio = {tarea.id: tarea.precio for tarea in tareas}

        return render(request, 'finish_Sell.html', {'lastSell': lastSell, 'consumos': consumos, 'tareas': tareas})
    else:
        tareas = Task.objects.filter(id__in=[consumo.producto.id for consumo in consumos])
        # Crear un diccionario que mapea id de tarea a precio
        id_to_precio = {tarea.id: tarea.precio for tarea in tareas}

        for consumo in consumos.values('cantidad', 'producto'):
            tarea_actual = Task.objects.get(id=consumo['producto'])

            # Obtener el precio asociado a la tarea
            precio_tarea = id_to_precio.get(tarea_actual.id, 0)  # Default a 0 si no se encuentra el precio

            # Crear la instancia de Sellsaved utilizando la instancia de Consumo y el precio
            sellSave = Sellsaved(
                user=usuario_actual,
                consumption=tarea_actual.id,  # Usar el ID de la tarea
                totalConsumption=precio_tarea,
                cantity=consumo['cantidad']
            )
            try:
                sellSave.save()
                deleteConsum= Consumo.objects.filter(user=usuario_actual)
                deleteConsum.delete()

        # Otras acciones después de guardar correctamente
        # ...

            except IntegrityError as e:
                print(f"Error al guardar: {e}")

        return redirect('home')
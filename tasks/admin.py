from django.contrib import admin
from .models import Task, Consumo
'''
class SubidaInline(admin.StackedInline):
    model = subida
    extra = 1  # Número de formularios en línea que se mostrarán

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user', 'created', 'datecompleted')
    inlines = [SubidaInline]  # Agregar la clase Inline aquí

    # Resto de la configuración de TaskAdmin

@admin.register(subida)
class SubidaAdmin(admin.ModelAdmin):
    list_display = ('id_image', 'image')
'''
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user', 'created', 'datecompleted', 'image', 'precio')

@admin.register(Consumo)
class ConsumoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad')
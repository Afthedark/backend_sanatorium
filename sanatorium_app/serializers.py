# gestion_proyectos/serializers.py
from rest_framework import serializers
from .models import Usuario, Proyecto, Tarea

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'rol']

class ProyectoSerializer(serializers.ModelSerializer):
    encargado = UsuarioSerializer()
    
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado', 'encargado']


class TareaSerializer(serializers.ModelSerializer):
    proyecto = ProyectoSerializer()
    empleado = UsuarioSerializer()
    
    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'proyecto', 'fecha', 'horas_invertidas', 'empleado', 'estado', 'archivo', 'orden']

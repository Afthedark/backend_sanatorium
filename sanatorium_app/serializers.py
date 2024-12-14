# gestion_proyectos/serializers.py
from rest_framework import serializers
from .models import Usuario, Proyecto, Tarea, Reporte, Metricas

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
        fields = ['id', 'titulo', 'descripcion', 'proyecto', 'fecha', 'horas_invertidas', 'empleado', 'estado', 'archivo']

class ReporteSerializer(serializers.ModelSerializer):
    proyecto = ProyectoSerializer()
    
    class Meta:
        model = Reporte
        fields = ['id', 'proyecto', 'contenido', 'fecha']

class MetricasSerializer(serializers.ModelSerializer):
    empleado = UsuarioSerializer()
    proyecto = ProyectoSerializer()
    
    class Meta:
        model = Metricas
        fields = ['id', 'empleado', 'proyecto', 'horas_trabajadas', 'tareas_completadas', 'fecha']

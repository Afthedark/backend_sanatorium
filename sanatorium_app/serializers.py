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

    # Este es para la actualización, pero ahora no solicitamos el estado y orden del cliente
    def update(self, instance, validated_data):
        # Los valores de estado y orden se manejan internamente en la vista
        instance.save()
        return instance

#En cada tarea no puede tener el mismo numero de orden  repetido 

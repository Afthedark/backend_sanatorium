from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Usuario, Proyecto, Tarea
from .serializers import UsuarioSerializer, ProyectoSerializer, TareaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    # Acción personalizada para actualizar el estado y la posición
    @action(detail=True, methods=['patch'])
    def mover_tarea(self, request, pk=None):
        tarea = self.get_object()  # Obtiene la tarea por ID

        # Obtener los datos enviados en la solicitud
        estado = request.data.get('estado')
        orden = request.data.get('orden')

        # Verifica si el estado o el orden fueron proporcionados
        if estado:
            tarea.estado = estado
        if orden is not None:
            tarea.orden = orden
        
        # Obtener todas las tareas del usuario que está relacionado con esta tarea
        tareas_usuario = Tarea.objects.filter(empleado=tarea.empleado)

        # Obtener todas las tareas del proyecto al que pertenece esta tarea
        tareas_proyecto = Tarea.objects.filter(proyecto=tarea.proyecto)

        # Guardar los cambios de la tarea
        tarea.save()

        # Responder con todos los datos relacionados en un solo objeto
        return Response({
            'id_proyecto': tarea.proyecto.id,
            'mensaje': 'Tarea movida correctamente',
            'tarea': TareaSerializer(tarea).data,
            'tareas_relacionadas': {
                'tareas_usuario': TareaSerializer(tareas_usuario, many=True).data,
                'tareas_proyecto': TareaSerializer(tareas_proyecto, many=True).data
            }
        }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # Obtener el proyecto y el usuario desde la solicitud
        proyecto = self.request.data.get('proyecto')
        empleado = self.request.data.get('empleado')

        # Obtener la última tarea para ese proyecto y usuario para calcular el nuevo orden
        last_tarea = Tarea.objects.filter(
            proyecto=proyecto,
            empleado=empleado,
            estado='pendiente'
        ).order_by('-orden').first()  # Obtenemos la última tarea de ese proyecto y empleado

        # Si existe una tarea previa, establecemos el orden de la nueva tarea
        if last_tarea:
            nuevo_orden = last_tarea.orden + 1
        else:
            nuevo_orden = 1  # Si no hay tareas, la nueva tarea será la primera

        # Crear la tarea con el estado "pendiente" y el nuevo orden calculado
        serializer.save(estado='pendiente', orden=nuevo_orden)

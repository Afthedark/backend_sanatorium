from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Usuario, Proyecto, Tarea, Metricas
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
        tarea = self.get_object()
        estado = request.data.get('estado')
        orden = request.data.get('orden')

        # Verifica si el estado o el orden fueron proporcionados
        if estado:
            tarea.estado = estado
        if orden is not None:
            tarea.orden = orden

        tarea.save()

        return Response({
            'mensaje': 'Tarea movida correctamente',
            'tarea': TareaSerializer(tarea).data
        }, status=status.HTTP_200_OK)




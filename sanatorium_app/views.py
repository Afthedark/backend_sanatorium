from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from rest_framework.decorators import api_view
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


#Custom API de actualizar tarea
@api_view(['POST'])
def actualizar_tarea(request):
    tarea_id = request.data.get('id')
    nuevo_estado = request.data.get('nuevo_estado')
    nuevo_orden = request.data.get('nuevo_orden')

    if not tarea_id or not nuevo_estado:
        return Response(
            {"error": "El ID de la tarea y el nuevo estado son obligatorios."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        tarea = Tarea.objects.get(id=tarea_id)

        # Validar estado
        if nuevo_estado not in dict(Tarea.ESTADOS_TAREA):
            return Response(
                {"error": f"Estado no válido. Valores permitidos: {list(dict(Tarea.ESTADOS_TAREA).keys())}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Actualizar estado y orden
        tarea.estado = nuevo_estado

        # Si se envía nuevo_orden, ajusta el orden de las demás tareas
        if nuevo_orden is not None:
            nuevo_orden = int(nuevo_orden)

            # Obtener todas las tareas del mismo estado excepto la actual
            tareas_misma_columna = Tarea.objects.filter(
                proyecto = tarea.proyecto,
                empleado = tarea.empleado,
                estado=nuevo_estado
            ).exclude(id=tarea_id).order_by('orden')

            # DEBUG no excluir la tarea actual

            # Ajustar los órdenes para incluir la tarea en la nueva posición
            tareas_actualizadas = []
            for i, t in enumerate(tareas_misma_columna, start=1):
                if i == nuevo_orden:  # Insertar la tarea actual en el nuevo orden
                    tarea.orden = i
                    tareas_actualizadas.append(tarea)
                    i += 1  # Incrementar para las siguientes tareas

                t.orden = i
                tareas_actualizadas.append(t)
            

            # Si el nuevo_orden es mayor que los existentes, simplemente colócala al final
            if nuevo_orden > len(tareas_misma_columna):
                tarea.orden = len(tareas_misma_columna) + 1
                tareas_actualizadas.append(tarea)

            # Guardar todas las tareas reordenadas
            Tarea.objects.bulk_update(tareas_actualizadas, ['orden'])

        else:
            # Si no se especifica un nuevo orden, coloca la tarea al final
            max_orden = Tarea.objects.filter(estado=nuevo_estado).aggregate(models.Max('orden'))['orden__max'] or 0
            tarea.orden = max_orden + 1

        tarea.save()
        serializer = TareaSerializer(tarea)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Tarea.DoesNotExist:
        return Response({"error": "Tarea no encontrada."}, status=status.HTTP_404_NOT_FOUND)

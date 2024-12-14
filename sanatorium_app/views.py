from django.shortcuts import render

# Create your views here.
# gestion_proyectos/views.py
from rest_framework import viewsets
from .models import Usuario, Proyecto, Tarea, Reporte, Metricas
from .serializers import UsuarioSerializer, ProyectoSerializer, TareaSerializer, ReporteSerializer, MetricasSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer

class MetricasViewSet(viewsets.ModelViewSet):
    queryset = Metricas.objects.all()
    serializer_class = MetricasSerializer


# sanatorium_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, ProyectoViewSet, TareaViewSet, actualizar_tarea

# Rutas automáticas
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'tareas', TareaViewSet)

# Rutas personalizadas
urlpatterns = [
    path('', include(router.urls)),  # CRUD automático
    path('custom/actualizar-tarea/', actualizar_tarea, name='actualizar_tarea'),  # Custom API
]

#Custom endpoints para crear, eliminar y actualizar tareas para todos desde el tunder client 

# sanatorium_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, ProyectoViewSet, TareaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'tareas', TareaViewSet)
#router.register(r'reportes', ReporteViewSet)
#router.register(r'metricas', MetricasViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

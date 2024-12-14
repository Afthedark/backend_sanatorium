from django.contrib import admin

from .models import Usuario, Proyecto, Tarea, Reporte, Metricas
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Proyecto)
admin.site.register(Tarea)
admin.site.register(Reporte)
admin.site.register(Metricas)
from django.db import models

# Create your models here.

# gestion_proyectos/models.py
from django.db import models

class Usuario(models.Model):
    ROLES = [
        ('administrador', 'Administrador'),
        ('encargado', 'Encargado de Proyecto'),
        ('empleado', 'Empleado'),
    ]
    
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, choices=ROLES)

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    ESTADOS = [
        ('completado', 'Completado'),
        ('en progreso', 'En progreso'),
        ('pendiente', 'Pendiente'),
    ]
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS)
    encargado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="proyectos_asignados")

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    ESTADOS_TAREA = [
        ('pendiente', 'Pendiente'),
        ('en progreso', 'En progreso'),
        ('completada', 'Completada'),
    ]
    
    titulo = models.CharField(max_length=255)  # Título de la tarea
    descripcion = models.TextField()  # Descripción de la tarea
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="tareas")  # Proyecto al que pertenece
    fecha = models.DateField()  # Fecha en que se registra la tarea
    horas_invertidas = models.IntegerField()  # Número de horas invertidas
    empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tareas_asignadas")  # El empleado que registra la tarea
    estado = models.CharField(max_length=20, choices=ESTADOS_TAREA)  # Estado de la tarea
    archivo = models.FileField(upload_to='archivos_tareas/', null=True, blank=True)  # Archivo opcional (documento, foto, etc.)
    orden = models.IntegerField(default=0)  # Campo para almacenar la posición de la tarea dentro de cada columna
    
    def __str__(self):
        return f"Tarea de {self.titulo} - {self.descripcion[:20]}"

class Metricas(models.Model):
    empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="metricas")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="metricas")
    horas_trabajadas = models.IntegerField()
    tareas_completadas = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return f"Métricas de {self.empleado.nombre} - {self.proyecto.nombre} - {self.fecha}"

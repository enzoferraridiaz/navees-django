from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Armador(models.Model):
    nombre = models.CharField(max_length=120)
    rut = models.CharField(max_length=12)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"


TIPO_NAVE = [
    ("LM", "Lancha menor"),
    ("PM", "Pesquera menor"),
    ("YT", "Yate"),
    ("OT", "Otro"),
] 
class Nave(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=2, choices=TIPO_NAVE, 
default="OT")
    eslora_m = models.DecimalField(max_digits=5, decimal_places=2, 
validators=[MinValueValidator(1)])
    anio = models.PositiveIntegerField(validators=[MinValueValidator(1950)])
    armador = models.ForeignKey(Armador, on_delete=models.PROTECT, related_name="naves")
    activa = models.BooleanField(default=True)

def __str__(self):
     return f"{self.nombre} [{self.matricula}]"

class Certificado(models.Model):
    nave = models.ForeignKey(Nave, on_delete=models.CASCADE, related_name="certificados")
    tipo = models.CharField(max_length=60)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()

class Meta:
    ordering = ["-fecha_vencimiento"]

@property
def vigente(self):
    return self.fecha_vencimiento >= timezone.localdate()

def clean(self):
    from django.core.exceptions import ValidationError
    if self.fecha_vencimiento <= self.fecha_emision:
       raise ValidationError("La fecha de vencimiento debe ser posterior a la emisión.")    
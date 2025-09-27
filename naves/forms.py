from django import forms
from .models import Nave, Certificado
from django import forms
from .models import Nave, Certificado
class NaveForm(forms.ModelForm):
   class Meta:
    model = Nave
    fields = ["matricula","nombre","tipo","eslora_m","anio","armador","activa"]
class CertificadoForm(forms.ModelForm):
  class Meta:
   model = Certificado
   fields = ["tipo","fecha_emision","fecha_vencimiento"]

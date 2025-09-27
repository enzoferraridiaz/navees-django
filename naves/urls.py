from django.urls import path
from . import views

app_name = "naves"

urlpatterns = [
    path("", views.NaveLista.as_view(), name="nave_list"),
    path("nave/nueva/", views.NaveCrear.as_view(), name="nave_create"),
    path("nave/<int:pk>/", views.NaveDetalle.as_view(), name="nave_detail"),
    path("nave/<int:pk>/editar/", views.NaveEditar.as_view(), name="nave_update"),
    path("nave/<int:pk>/eliminar/", views.NaveEliminar.as_view(), name="nave_delete"),
    path("nave/<int:pk>/certificado/nuevo/", views.CertificadoCrear.as_view(), name="cert_create"),
    path("certificado/<int:pk>/editar/", views.CertificadoEditar.as_view(), name="cert_update"),
    path("certificado/<int:pk>/eliminar/", views.CertificadoEliminar.as_view(), name="cert_delete"),
]
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Nave, Certificado
from .forms import NaveForm, CertificadoForm


class NaveLista(ListView):
    model = Nave
    paginate_by = 10
    template_name = "naves/nave_list.html"  # Opcional, si quieres un template personalizado

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        tipo = self.request.GET.get("tipo")

        if q:
            queryset = queryset.filter(
                Q(matricula__icontains=q) |
                Q(nombre__icontains=q) |
                Q(armador__nombre__icontains=q)
            )

        if tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset


class NaveDetalle(DetailView):
    model = Nave
    template_name = "naves/nave_detail.html"


class NaveCrear(CreateView):
    model = Nave
    form_class = NaveForm
    template_name = "naves/nave_form.html"
    success_url = reverse_lazy("naves:nave_list")


class NaveEditar(UpdateView):
    model = Nave
    form_class = NaveForm
    template_name = "naves/nave_form.html"
    success_url = reverse_lazy("naves:nave_list")


class NaveEliminar(DeleteView):
    model = Nave
    template_name = "naves/nave_confirm_delete.html"
    success_url = reverse_lazy("naves:nave_list")


class CertificadoCrear(CreateView):
    model = Certificado
    form_class = CertificadoForm
    template_name = "naves/certificado_form.html"

    def get_success_url(self):
        return reverse_lazy("naves:nave_detail", kwargs={"pk": self.object.nave.pk})


class CertificadoEditar(UpdateView):
    model = Certificado
    form_class = CertificadoForm
    template_name = "naves/certificado_form.html"

    def get_success_url(self):
        return reverse_lazy("naves:nave_detail", kwargs={"pk": self.object.nave.pk})


class CertificadoEliminar(DeleteView):
    model = Certificado
    template_name = "naves/certificado_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("naves:nave_detail", kwargs={"pk": self.object.nave.pk})

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

# Create your views here.
from django.db.models import Count, Q
from django.utils import timezone
from django.views.generic import ListView
from .models import Nave


class NaveLista(ListView):
    model = Nave
    paginate_by = 10
    template_name = "naves/nave_list.html"

    def dispatch(self, request, *args, **kwargs):
        # Guardar la fecha actual en request para usar en annotate
        self.request.today = timezone.localdate()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get("q")
        tipo = self.request.GET.get("tipo")
        activa = self.request.GET.get("activa")

        qs = (
            Nave.objects
            .select_related("armador")
            .annotate(
                cert_vigentes=Count(
                    "certificados",
                    filter=Q(certificados__fecha_vencimiento__gte=self.request.today)
                )
            )
        )

        if q:
            qs = qs.filter(
                Q(matricula__icontains=q) |
                Q(nombre__icontains=q) |
                Q(armador__nombre__icontains=q)
            )

        if tipo:
            qs = qs.filter(tipo=tipo)

        if activa in ("true", "false"):
            qs = qs.filter(activa=(activa == "true"))

        return qs.order_by("nombre")
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import Nave, Certificado
from .forms import NaveForm, CertificadoForm


class NaveDetalle(DetailView):
    model = Nave
    template_name = "naves/nave_detail.html"

    def get_queryset(self):
        return (
            Nave.objects
            .select_related("armador")
            .prefetch_related("certificados")
        )


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
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Certificado
from .forms import CertificadoForm


class CertificadoEditar(UpdateView):
    model = Certificado
    form_class = CertificadoForm
    template_name = "naves/certificado_form.html"

    def form_valid(self, form):
        # Asegura que el certificado esté asociado a la nave correcta
        form.instance.nave_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige a la página de detalle de la nave asociada
        return reverse_lazy("naves:nave_detail", kwargs={"pk": self.kwargs["pk"]})
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import Certificado
from .forms import CertificadoForm


class CertificadoEditar(UpdateView):
    model = Certificado
    form_class = CertificadoForm
    template_name = "naves/certificado_form.html"

    def get_success_url(self):
        # Redirige a la vista de detalle de la nave asociada
        return reverse_lazy("naves:nave_detail", kwargs={"pk": self.object.nave_id})


class CertificadoEliminar(DeleteView):
    model = Certificado
    template_name = "naves/certificado_confirm_delete.html"

    def get_success_url(self):
        # Redirige a la vista de detalle de la nave asociada
        return reverse_lazy("naves:nave_detail", kwargs={"pk": self.object.nave_id})

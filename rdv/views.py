from functools import wraps
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST
from .forms import CreneauForm, RendezVousForm, SignupForm
from .models import Creneau, RendezVous, Service


# Create your views here.
def gestionnaire_requis(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper


def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        messages.success(request, "Compte créé.")
        return redirect("creneaux")
    return render(request, "registration/signup.html", {"form": form})


def creneaux(request):
    now = timezone.localtime()
    qs = (Creneau.objects.filter(ouvert=True)
          .filter(Q(date__gt=now.date()) | Q(date=now.date(), heure_debut__gt=now.time()))
          .exclude(rendezvous__statut=RendezVous.RESERVE)
          .select_related("service"))
    service_id = request.GET.get("service", "")
    date = request.GET.get("date", "")
    if service_id.isdigit():
        qs = qs.filter(service_id=service_id)
    if date and parse_date(date):
        qs = qs.filter(date=parse_date(date))
    page = Paginator(qs, 10).get_page(request.GET.get("page"))
    return render(request, "creneau_list.html", {
        "page_obj": page, "services": Service.objects.all(),
        "service_id": service_id, "date": date})


@login_required
def reserver(request, pk):
    creneau = get_object_or_404(Creneau, pk=pk)
    if not creneau.est_reservable:
        messages.error(request, "Ce créneau n'est plus réservable.")
        return redirect("creneaux")
    form = RendezVousForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        rdv = form.save(commit=False)
        rdv.creneau, rdv.utilisateur = creneau, request.user
        try:
            with transaction.atomic():
                rdv.save()
        except IntegrityError:  # quelqu'un a réservé entre-temps
            messages.error(request, "Ce créneau vient d'être pris.")
            return redirect("creneaux")
        messages.success(request, "Rendez-vous confirmé.")
        return redirect("mes_rdv")
    return render(request, "reserver.html", {"form": form, "creneau": creneau})


@login_required
def mes_rdv(request):
    qs = request.user.rendezvous.select_related("creneau__service")
    return render(request, "mes_rdv.html", {"page_obj": Paginator(qs, 10).get_page(request.GET.get("page"))})


@login_required
@require_POST
def annuler(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk, utilisateur=request.user)  # 404 si pas le sien
    if rdv.peut_annuler:
        rdv.statut = RendezVous.ANNULE
        rdv.save()
        messages.success(request, "Rendez-vous annulé.")
    else:
        messages.error(request, "Annulation impossible (déjà commencé ou non réservé).")
    return redirect("mes_rdv")


@gestionnaire_requis
def creneau_creer(request):
    form = CreneauForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Créneau créé.")
        return redirect("agenda")
    return render(request, "creneau_form.html", {"form": form})


@gestionnaire_requis
def agenda(request):
    qs = RendezVous.objects.select_related("creneau__service", "utilisateur")
    statut = request.GET.get("statut", "")
    if statut:
        qs = qs.filter(statut=statut)
    page = Paginator(qs, 15).get_page(request.GET.get("page"))
    return render(request, "agenda.html", {"page_obj": page, "statuts": RendezVous.STATUTS})


@gestionnaire_requis
@require_POST
def marquer(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk)
    statut = request.POST.get("statut")
    if rdv.statut == RendezVous.RESERVE and statut in (RendezVous.REALISE, RendezVous.ABSENT):
        rdv.statut = statut
        rdv.save()
        messages.success(request, "Statut mis à jour.")
    else:
        messages.error(request, "Transition non autorisée.")
    return redirect("agenda")
import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

# Create your models here.
class Service(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Creneau(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="creneaux")
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    ouvert = models.BooleanField(default=True)

    class Meta:
        ordering = ["date", "heure_debut"]

    def __str__(self):
        return f"{self.service} {self.date} {self.heure_debut:%H:%M}-{self.heure_fin:%H:%M}"

    def clean(self):
        if self.heure_debut and self.heure_fin and self.heure_fin <= self.heure_debut:
            raise ValidationError("L'heure de fin doit être après l'heure de début.")

    @property
    def debut(self):
        return timezone.make_aware(datetime.datetime.combine(self.date, self.heure_debut))

    @property
    def est_reservable(self):
        return (self.ouvert and self.debut > timezone.now()
                and not self.rendezvous.filter(statut=RendezVous.RESERVE).exists())


class RendezVous(models.Model):
    RESERVE, ANNULE, REALISE, ABSENT = "reserve", "annule", "realise", "absent"
    STATUTS = [(RESERVE, "Réservé"), (ANNULE, "Annulé"),
               (REALISE, "Réalisé"), (ABSENT, "Absent")]

    creneau = models.ForeignKey(Creneau, on_delete=models.CASCADE, related_name="rendezvous")
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name="rendezvous")
    motif = models.CharField(max_length=255)
    statut = models.CharField(max_length=10, choices=STATUTS, default=RESERVE)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["creneau__date", "creneau__heure_debut"]
        constraints = [models.UniqueConstraint(
            fields=["creneau"], condition=Q(statut="reserve"),
            name="un_seul_rdv_reserve_par_creneau")]

    @property
    def peut_annuler(self):
        return self.statut == self.RESERVE and self.creneau.debut > timezone.now()
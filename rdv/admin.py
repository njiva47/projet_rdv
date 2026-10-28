from django.contrib import admin
from .models import Service, Creneau, RendezVous

admin.site.register(Service)

@admin.register(Creneau)
class CreneauAdmin(admin.ModelAdmin):
    list_display = ("service", "date", "heure_debut", "heure_fin", "ouvert")
    list_filter = ("service", "date", "ouvert")

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ("creneau", "utilisateur", "statut")
    list_filter = ("statut",)
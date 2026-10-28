from django.urls import path
from . import views

urlpatterns = [
    path("", views.creneaux, name="creneaux"),
    path("inscription/", views.signup, name="signup"),
    path("reserver/<int:pk>/", views.reserver, name="reserver"),
    path("mes-rdv/", views.mes_rdv, name="mes_rdv"),
    path("annuler/<int:pk>/", views.annuler, name="annuler"),
    path("gestion/creneaux/nouveau/", views.creneau_creer, name="creneau_creer"),
    path("gestion/agenda/", views.agenda, name="agenda"),
    path("gestion/marquer/<int:pk>/", views.marquer, name="marquer"),
]
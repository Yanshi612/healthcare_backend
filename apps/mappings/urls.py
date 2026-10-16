from django.urls import path

from .views import MappingByPatientView, MappingDeleteView, MappingListCreateView

urlpatterns = [
    path("", MappingListCreateView.as_view(), name="mapping-list-create"),
    path("<uuid:patient_id>/", MappingByPatientView.as_view(), name="mapping-by-patient"),
    path("remove/<uuid:pk>/", MappingDeleteView.as_view(), name="mapping-delete"),
]

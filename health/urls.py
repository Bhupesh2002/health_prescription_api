from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    FamilyMemberViewSet,
    MedicineViewSet,
    PrescriptionViewSet,
    MedicationLogViewSet,
    TodayMedicineViewSet,
    mark_as_taken,
    register_user
)


router = DefaultRouter()
router.register('family', FamilyMemberViewSet)
router.register('medicines', MedicineViewSet)
router.register('prescriptions', PrescriptionViewSet)
router.register('logs', MedicationLogViewSet)
router.register('today-medicines', TodayMedicineViewSet, basename='today-medicines')

urlpatterns = [
    path('register/', register_user),
    path('mark_as_taken/',mark_as_taken),
]

urlpatterns += router.urls   
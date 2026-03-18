from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    FamilyMemberViewSet,
    MedicineViewSet,
    PrescriptionViewSet,
    MedicationLogViewSet,
    TodayMedicineViewSet,
    mark_as_taken
)

urlpatterns = [
    path('mark_as_taken/',mark_as_taken),
]

router = DefaultRouter()
router.register('family', FamilyMemberViewSet)
router.register('medicines', MedicineViewSet)
router.register('prescriptions', PrescriptionViewSet)
router.register('logs', MedicationLogViewSet)
router.register('today-medicines', TodayMedicineViewSet, basename='today-medicines')

urlpatterns = router.urls   
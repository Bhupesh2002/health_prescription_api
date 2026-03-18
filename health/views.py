from rest_framework.decorators import api_view, permission_classes
from datetime import date
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import FamilyMember, Medicine, Prescription, MedicationLog
from .serializer import (
    FamilyMemberSerializer,
    MedicineSerializer,
    PrescriptionSerializer,
    MedicationLogSerializer,
    TodayMedicineSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Create your views here.

class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filter_fields = ['relation']
    search_fields = ['name', 'relation']

    def get_queryset(self):
        return FamilyMember.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'dosage']


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['family_member','medicine']
    search_fields = ['medicine__name', 'family_member__name']

    def get_queryset(self):
        return Prescription.objects.filter(
            family_member__user=self.request.user
        )
    
class MedicationLogViewSet(viewsets.ModelViewSet):
    queryset = MedicationLog.objects.all()  
    serializer_class = MedicationLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MedicationLog.objects.filter(
            prescription__family_member__user=self.request.user
        )
    
class TodayMedicineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TodayMedicineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        today = date.today()
        return Prescription.objects.filter(
            family_member__user=self.request.user,
            start_date__lte=today,
            end_date__gte=today
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_taken(request):
    prescription_id = request.data.get('prescription_id')

    try:
        prescription = Prescription.objects.get(
            id=prescription_id,
            family_member__user=request.user
        )
    except Prescription.DoesNotExist:
        return Response({"error": "Invalid prescription"}, status=404)

    today = date.today()

    log, created = MedicationLog.objects.get_or_create(
        prescription=prescription,
        date=today,
        defaults={'status': 'taken'}
    )

    if not created:
        log.status = 'taken'
        log.save()

    return Response({"message": "Medicine marked as taken"})
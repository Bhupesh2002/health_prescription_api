from django.contrib import admin
from .models import FamilyMember, Medicine, Prescription, MedicationLog

# Register your models here.

admin.site.register(FamilyMember)
admin.site.register(Medicine)
admin.site.register(Prescription)
admin.site.register(MedicationLog)

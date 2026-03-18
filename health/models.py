from django.db import models
from django.contrib.auth.models import User

class FamilyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_members')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    relation = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.relation})"
    
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Prescription(models.Model):
    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.medicine.name} for {self.family_member.name}"
    

class MedicationLog(models.Model):
    STATUS_CHOICES = (
        ('taken', 'Taken'),
        ('missed', 'Missed'),
    )

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.prescription} - {self.status}"
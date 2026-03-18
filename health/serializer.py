from rest_framework import serializers
from .models import FamilyMember, Medicine, Prescription, MedicationLog
from django.contrib.auth.models import User

class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '__all__'
        read_only_fields = ['user']

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


class MedicationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationLog
        fields = '__all__'

class TodayMedicineSerializer(serializers.ModelSerializer):
    family_member = serializers.CharField(source='family_member.name', read_only=True)
    medicine = serializers.CharField(source='medicine.name', read_only=True)
    dosage = serializers.CharField(source='medicine.dosage', read_only=True)

    class Meta:
        model = Prescription
        fields = ['family_member', 'medicine', 'dosage', 'time']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

        
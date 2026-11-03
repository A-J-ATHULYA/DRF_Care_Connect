from rest_framework import serializers
from clinic.models import DoctorDb, AppointmentDb
from django.utils import timezone

class Doctor_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDb
        #fields = ["id", "Doctor_name",.....]
        fields = "__all__"
        read_only_fields = ["id"]
        
        
class Appointment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentDb
        fields = "__all__"
        read_only_fields = ["id"]
        
    def validate(self, validated_data):
        phone = validated_data.get("Contact_number")
        appointment_date = validated_data.get("Appointment_date")
        
        if appointment_date < timezone.localdate():
            raise serializers.ValidationError("Invalid Date")
        
        if AppointmentDb.objects.filter(
            Contact_number = phone, Appointment_date=appointment_date).exists():
            raise serializers.ValidationError("Already Booked")
        
        else:
            return validated_data
        
        
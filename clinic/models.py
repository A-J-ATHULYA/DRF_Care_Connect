from django.db import models

# Create your models here.

class DoctorDb(models.Model):
    
    Doctor_name = models.CharField(max_length=400)
    
    Specialization = models.CharField(max_length=400)
    
    Experience = models.PositiveIntegerField()
    
    Hospital = models.CharField(max_length=400)
    
    # Qualification = models.CharField(max_length=500)
    
    Consultation_Fee = models.PositiveIntegerField()
    
    Available = models.BooleanField()
    
    def __str__(self):
        return self.Doctor_name
    
  
class AppointmentDb(models.Model):
    
    Patient_name = models.CharField(max_length=400)
    
    Age = models.IntegerField()
    
    Gender = models.CharField(max_length=100)
    
    Contact_number = models.CharField(max_length=400)
    
    Doctor_id = models.IntegerField()
    
    Appointment_date = models.DateField()
    
    Token_number = models.PositiveIntegerField(editable=False, null=True)
    
    Appointment_time = models.TimeField(editable=False, null=True)
    
    Problem = models.TextField()
    
    Status = models.CharField(max_length=200, default="Pending")
    
    Prescription = models.TextField(null=True, blank=True)
    
    Created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Patient_name
  
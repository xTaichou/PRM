from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postal = models.IntegerField(default=0)
    employeesc = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class CompanyBilling(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    postal = models.IntegerField(default=0)
    amount = models.DecimalField(default=0, decimal_places=3, max_digits=6)
    outstanding = models.IntegerField(default=0)
    lastInvoice = models.DateField('Last Invoice')
    nextInvoice = models.DateField('Next Invoice')

    def __str__(self):
        return self.company


class Employees(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    groups = (("Manager", "Manager"),("Practitioner", "Practitioner"),("User", "User"))
    group = models.CharField(max_length=12, choices=groups, default="User")
    email = models.EmailField()
    phone = models.IntegerField(default=0000000000)
    password = models.CharField(max_length=200)

    def __str__(self):
        fullname = (f"{self.firstname} {self.surname}")
        return fullname


class Patients(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField(default=0000000000)
    dob = models.DateField('Date of Birth',default=date.today)
    idNumber = models.CharField(max_length=13)
    address = models.CharField(max_length=200, default='JHB')
    medicalAid = models.BooleanField()
    maidName = models.CharField(max_length=25, blank=True, default='Basic')
    maidNumber = models.CharField(max_length=15, blank=True, default='0000')
    password = models.CharField(max_length=200)

    def __str__(self):
        fullname = (f"{self.firstname} {self.surname}")
        return fullname

class MedicalData(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    familyCancer = models.BooleanField(default=False)
    familyCancerNotes = models.CharField(max_length=500, blank=True,default='None')
    pastSurgery = models.BooleanField(default=False)
    pastSurgeryNotes = models.CharField(max_length=1000,blank=True,default='None')
    chronicIllness = models.BooleanField(default=False)
    chronicIllnessNotes = models.CharField(max_length=1000, blank=True,default='None')
    medication = models.CharField(max_length=1000, blank=True, default='None')
    otherNotes = models.CharField(max_length=1000, blank=True, default='None')
    files = models.FileField(blank=True)

    def __str__(self):
        return self.patient.__str__()

class DataDictionary(models.Model):
    item = models.CharField(max_length=200)
    definition = models.CharField(max_length=200)
    symptoms = models.CharField(max_length=200)
    recommendations = models.CharField(max_length=200)

class Bookings(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Employees, on_delete=models.CASCADE)
    date = models.DateTimeField('Booking date&time')

class Visits(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Employees, on_delete=models.CASCADE)
    date = models.DateTimeField('Visit date')
    reason = models.CharField(max_length=200)
    prognosis = models.CharField(max_length=1000)
    notes = models.CharField(max_length=1000, default="N/A", blank=True)
    perscription = models.BooleanField()
    files = models.FileField(blank=True)

    def __str__(self):
        return self.patient.__str__()
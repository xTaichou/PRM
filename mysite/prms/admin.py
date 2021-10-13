from django.contrib import admin
from .models import Company, Employees, Patients, MedicalData, CompanyBilling, Visits

admin.site.register(Company)
admin.site.register(Employees)
admin.site.register(Patients)
admin.site.register(MedicalData)
admin.site.register(CompanyBilling)
admin.site.register(Visits)
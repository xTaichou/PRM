from django.forms import ModelForm, PasswordInput, DateTimeInput, Textarea, HiddenInput, DateInput
from .models import Patients, Company, Employees, CompanyBilling, Bookings, Visits, MedicalData
from django import forms
from django.contrib.auth import get_user_model
from datetimepicker.widgets import DateTimePicker

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = ['company','firstname', 'surname', 'email', 'phone', 'password']
        widgets = {'password': PasswordInput()}

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['company','firstname', 'surname', 'email', 'phone', 'password', 'group']
        widgets = {'password': PasswordInput()}

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'postal', 'employeesc']

class CompanyBillingForm(forms.ModelForm):
    class Meta:
        model = CompanyBilling
        fields = ['company', 'address', 'postal', 'lastInvoice', 'nextInvoice']
        widgets = {'lastInvoice': DateInput(), 'nextInvoice': DateInput()}

class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['doctor', 'patient', 'date']
        widgets = {'date': DateInput()}

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visits
        fields = ['doctor', 'patient', 'date', 'reason', 'prognosis', 'perscription', 'notes', 'files']
        widgets = {'doctor': HiddenInput, 'patient': HiddenInput, "date": DateTimeInput(),
                   "reason": Textarea(), "prognosis": Textarea(), "notes": Textarea()}



User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    # def clean(self):
    #     data = super().clean()
    #     username = data.get("username")
    #     password = data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)  # thisIsMyUsername == thisismyusername
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        if qs.count() != 1:
            raise forms.ValidationError("This is an invalid user.")
        return username

class MedForm(forms.ModelForm):
    class Meta:
        model = MedicalData
        fields = '__all__'
        widgets = {'patient': HiddenInput}
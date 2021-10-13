from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from datetime import datetime, date
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required

from .forms import PatientForm, CompanyForm, EmployeeForm, CompanyBillingForm, LoginForm, BookingForm, VisitForm, MedForm
from .models import Patients, Company, Employees, DataDictionary, MedicalData, Visits
from django.contrib.auth.forms import UserCreationForm

comp = ""
User = get_user_model()


def index(request):
    template = loader.get_template('prms/index.html')
    return render(request, 'prms/index.html')


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            # user is valid and active -> is_active
            # request.user == user
            login(request, user)
            print(user.groups)
            if user.groups.filter(name='Manager').exists():
                return redirect('manager')
            elif user.groups.filter(name='User').exists():
                return redirect('user')
            else:
                return redirect('practitioner')
        else:
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] = attempt + 1
            # return redirect("/invalid-password")
            request.session['invalid_user'] = 1 # 1 == True
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')

def patient_create(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        print('Saved')
        form.save()
        form = EmployeeForm()
    context = {'form': form}
    return render(request, 'prms/patient/create.html', context)

def company_create(request):
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        comp = form.cleaned_data.get("name")
        form.save()
        return redirect(f'/company_billing/{comp}', company_name=comp)
    context = {'form': form}
    return render(request, 'prms/company/create.html', context)

def employee_create(request, company_name=""):
    form = EmployeeForm(request.POST or None)
    if company_name != "":
        compObj = Company.objects.get(name=company_name)
        form = EmployeeForm(request.POST or None, initial={'company': compObj, 'group': 'Manager'})
    if form.is_valid():
        print(form.cleaned_data.get("group"))
        user = User.objects.create_user(form.cleaned_data.get("email"), form.cleaned_data.get("email"), form.cleaned_data.get("password"))
        group = Group.objects.get(name=form.cleaned_data.get("group"))
        user.groups.add(group)
        form.save()
        form = EmployeeForm()
    context = {'form': form}
    return render(request, 'prms/employee/create.html', context)

def company_billing(request, company_name=""):
    form = CompanyBillingForm(request.POST or None)
    date = datetime.today().strftime('%Y-%m-20')
    if company_name != "":
        compObj = Company.objects.get(name=company_name)
        form = CompanyBillingForm(request.POST or None,
                              initial={'company': compObj,
                                         'address': compObj.address,
                                         'postal': compObj.postal,
                                         'lastInvoice': date,
                                         'nextInvoice': date})
    if form.is_valid():
        form.save()
        return redirect(f'/employee_create/{company_name}', company_name=comp)
    context = {'form': form}
    return render(request, 'prms/company/billing.html', context)

@login_required(login_url='login')
def manager(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request,'prms/dashboards/ManagerD.html')


def user(request):
    return render(request,'prms/dashboards/UserD.html')


def practitioner(request):
    return render(request,'prms/dashboards/PracD.html')


def calendar(request):
    return render(request,'prms/dashboards/calendar.html')


def patient_list(request):
    return render(request,'prms/dashboards/UserD.html')


def all_patients(request):
    user = Employees.objects.get(email=request.user.email)
    patients = Patients.objects.all().filter(company=user.company)
    context = {'patients': patients}
    return render(request, 'prms/patient/all_patients.html', context)


def inventory(request):
    return render(request,'prms/inventory/list.html')


def employee_list(request):
    user = Employees.objects.get(email=request.user.email)
    employees = Employees.objects.all().filter(company=user.company)
    context = {'employees': employees}
    return render(request,'prms/employee/employees.html', context)

def dictionary_list(request):
    return render(request,'prms/dictionary/list.html')

def d_more(request, id):
    data = DataDictionary.objects.get(pk=id)
    context = {'data': data}
    return render(request,'prms/dictionary/more.html', context)

def e_edit(request, id):
    data = Employees.objects.get(pk=id)
    context = {'data': data}
    return render(request,'prms/employees/edit.html', context)

def new_booking(request):
    user = Employees.objects.get(email=request.user.email)
    employees = Employees.objects.all().filter(company=user.company)
    doctors = Employees.objects.all().filter(company=user.company, group='Practitioner')
    patients = Patients.objects.all().filter(company=user.company)
    filter = {'doctor': doctors, 'patient': patients}
    print(doctors, patients)

    form = BookingForm(request.POST or None, initial=filter)
    if form.is_valid():
        form.save()
        form = EmployeeForm()
    context = {'employees': employees, 'doctors': doctors, 'form': form}
    return render(request,'prms/bookings/new.html', context)

def p_view(request, id):
    patient = Patients.objects.get(pk=id)
    visit = Visits.objects.all().filter(patient=patient).order_by('-date')
    last = Visits.objects.all().filter(patient=patient).latest('date')
    medData = ""
    try:
        medData = MedicalData.objects.get(patient=patient)
        context = {'patient': patient, "visits": visit, 'last': last, "medData": medData}
        print(medData)
    except:
        context = {'patient': patient, "visits": visit, 'last': last, "medData": False}

    print("med data", medData)
    return render(request,'prms/patient/view.html', context)

def new_visit(request, id):
    user = Employees.objects.get(email=request.user.email)
    patients = Patients.objects.get(pk=id)
    filter = {'doctor': user, 'patient': patients, 'date': datetime.now()}

    form = VisitForm(request.POST or None, initial=filter)
    if form.is_valid():
        print("Valid")
        form.save()
        return redirect(f'/p_view/{id}')
    elif request.POST:
        print("Invalid", form.cleaned_data.get("doctor"))
    context = {'employees': user, 'patient': patients, 'form': form}
    return render(request, 'prms/visits/Add.html', context)

def edit_visit(request, id):
    data = Visits.objects.get(pk=id)
    patients = data.patient
    filter = {'doctor': request.user,
              'patient': patients,
              'date': data.date,
              'reason': data.reason,
              'prognosis': data.prognosis,
              'notes': data.notes,
              'perscription': data.perscription}
    form = VisitForm(request.POST or None, initial=filter)
    if form.is_valid():
        data.date = form.cleaned_data.get('date')
        data.reason = form.cleaned_data.get('reason')
        data.prognosis = form.cleaned_data.get('prognosis')
        data.notes = form.cleaned_data.get('notes')
        data.perscription = form.cleaned_data.get('perscription')

        data.save()
        return redirect(f'/p_view/{data.patient.id}')
    context = {'data': data, 'form': form}
    return render(request,'prms/visits/edit.html', context)

def delete_visit(request, id):
    user = Employees.objects.get(email=request.user.email)
    Visits.objects.filter(pk=id).delete()
    return redirect(f'/p_view/{user.pk}')

def edit_med(request, id):
    user = Employees.objects.get(email=request.user.email)
    patient = Patients.objects.get(pk=id)
    form = MedForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = EmployeeForm()
    context = {'patient': patient, 'form': form}
    return render(request, 'prms/med-data/edit.html', context)

def add_med(request, id):
    user = Employees.objects.get(email=request.user.email)
    patient = Patients.objects.get(pk=id)
    filter = {'patient': patient}
    form = MedForm(request.POST or None, initial=filter)
    if form.is_valid():
        form.save()
        return redirect(f'/p_view/{id}')
    else:
        print('invalid')
    context = {'patient': patient, 'form': form}
    return render(request, 'prms/med-data/add.html', context)
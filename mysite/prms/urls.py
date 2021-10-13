from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('patient_create', views.patient_create, name='pcreate'),
    path('employee_create/<str:company_name>', views.employee_create, name='ecreate'),
    path('employee_list', views.employee_list, name='employees'),
    path('company_create', views.company_create, name='ccreate'),
    path('company_billing/<str:company_name>', views.company_billing, name='billing'),
    path('manager', views.manager, name='manager'),
    path('user', views.user, name='user'),
    path('practitioner', views.practitioner, name='practitioner'),
    path('calendar', views.calendar, name='calendar'),
    path('patient_list', views.patient_list, name='patient_list'),
    path('all_patients', views.all_patients, name='all_patients'),
    path('inventory', views.inventory, name='inventory'),
    path('dictionary', views.dictionary_list, name='dictionary'),
    path('d_more/<int:id>', views.d_more, name='d_more'),
    path('e_edit/<int:id>', views.e_edit, name='e_edit'),
    path('n_booking', views.new_booking, name='n_booking'),
    path('p_view/<int:id>', views.p_view, name='p_view'),
    path('new_visit/<int:id>', views.new_visit, name='new_visit'),
    path('edit_visit/<int:id>', views.edit_visit, name='edit_visit'),
    path('delete_visit/<int:id>', views.delete_visit, name='delete_visit'),
    path('add_med/<int:id>', views.add_med, name='add_med'),
    path('edit_med/<int:id>', views.edit_med, name='edit_med'),
]


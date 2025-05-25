
from  django.urls  import path
from  main.authentication.auth import  register_user,logout_user,login_user
from main.add_family_member.add_member import add_family_member
from main.edit_family_members.edit_members import edit_family_members
from main.delete_family_members.delete_members import delete_family_members
from  django.views.generic import  TemplateView
from  main.get_user_details.get_details import get_user_profile
from  main.get_family_members_details.family_details  import get_family_member_details
from  main.get_all_category.category_views import get_category_name
from  main.doctor_login_register.doctor_auth import  register_view_of_doctors,login_view_for_doctor
from  main.show_doctor_details.show_details import  get_doctor_details
from  main.search_doctors.search_views import searh_doctors_by_category
from  main.book_appointment_with_doctor.appointment_views import request_appointment
from  main.request_appointment_views.request_appointment_views import listed_appointments

urlpatterns = [
    # Serve templates at root paths (for frontend display)
    path('', TemplateView.as_view(template_name='main/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='main/register.html'), name='register'),

    # Actual API endpoints (used in fetch)
    path('api/register/', register_user, name='register_api'),
    path('api/login/', login_user, name='login_api'),
    path('logout/', logout_user, name='logout'),


    path('edit_family_member/<int:member_id>/',TemplateView.as_view(template_name='main/edit_family_member.html'),name='edit_member'),
    path('api/edit_family_member/<int:member_id>/', edit_family_members, name='edit_family_member'),
    path('delete-family-member/<int:member_id>/', delete_family_members, name='delete_family_member'),

    # endpoint for the userprofile 
    path('user_details/',TemplateView.as_view(template_name='main/user_details.html'),name='user_details'),
    path('api/user-details/', get_user_profile, name='get_user_details'),

    path('add_family_member/', TemplateView.as_view(template_name='main/add_family_member.html'), name='add_family_member'),

    path('api/add-family-members/', add_family_member, name='add_family_members'),

    path('api/get-family-details/<int:member_id>/',get_family_member_details,name='family-details'),

    path('api/categories/', get_category_name,name="category_name"),

    path('api/doctor-register/', register_view_of_doctors,name="doctor-register"),
    path('api/doctor-login/', login_view_for_doctor,name="doctor-login"),

    path('doctor_login/', TemplateView.as_view(template_name='main/doctor_login.html'), name='doctor_login'),
    path('doctor_registration/', TemplateView.as_view(template_name='main/doctor_registration.html'), name='doctor_registration'),

    path('doctor_details/',TemplateView.as_view(template_name='main/doctor_details.html'),name='doctor_details'),
    path('api/all-doctors/', get_doctor_details, name='list_all_doctors'),
    path('api/search-doctors/', searh_doctors_by_category, name='search_doctors'),

    path('api/request-appointment/<int:doctor_id>/', request_appointment, name='request_appointment'),
    path('api/doctor-appointments/', listed_appointments, name='doctor_appointments')

    



]


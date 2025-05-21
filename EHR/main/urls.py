
from  django.urls  import path
from  main.authentication.auth import  register_user,logout_user,login_user
from main.add_family_member.add_member import add_family_member
from main.edit_family_members.edit_members import edit_family_members
from main.delete_family_members.delete_members import delete_family_members
from  django.views.generic import  TemplateView
from  main.get_user_details.get_details import get_user_profile
urlpatterns = [
    # Serve templates at root paths (for frontend display)
    path('login/', TemplateView.as_view(template_name='main/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='main/register.html'), name='register'),

    # Actual API endpoints (used in fetch)
    path('api/register/', register_user, name='register_api'),
    path('api/login/', login_user, name='login_api'),
    path('logout/', logout_user, name='logout'),

    path('edit-family-member/<int:member_id>/', edit_family_members, name='edit_family_member'),
    path('delete-family-member/<int:member_id>/', delete_family_members, name='delete_family_member'),

    # endpoint for the userprofile 
    path('user_details/',TemplateView.as_view(template_name='main/user_details.html'),name='user_details'),
    path('api/user-details/', get_user_profile, name='get_user_details'),

    path('add_family_member/', TemplateView.as_view(template_name='main/add_family_member.html'), name='add_family_member'),

    path('api/add-family-members/', add_family_member, name='add_family_members'),
]


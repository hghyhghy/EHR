
from  django.urls  import path
from  main.authentication.auth import  register_user,logout_user,login_user
from main.add_family_member.add_member import add_family_members
from main.edit_family_members.edit_members import edit_family_members
from main.delete_family_members.delete_members import delete_family_members
from  django.views.generic import  TemplateView
urlpatterns = [
    # Serve templates at root paths (for frontend display)
    path('login/', TemplateView.as_view(template_name='main/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='main/register.html'), name='register'),

    # Actual API endpoints (used in fetch)
    path('api/register/', register_user, name='register_api'),
    path('api/login/', login_user, name='login_api'),
    path('logout/', logout_user, name='logout'),

    path('add-family-members/', add_family_members, name='add_family_member'),
    path('edit-family-member/<int:member_id>/', edit_family_members, name='edit_family_member'),
    path('delete-family-member/<int:member_id>/', delete_family_members, name='delete_family_member'),
]


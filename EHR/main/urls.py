
from  django.urls  import path
from  main.authentication.auth import  register_user,logout_user,login_user
from main.add_family_member.add_member import add_family_members
from main.edit_family_members.edit_members import edit_family_members
urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # endpoint for adding family member
    path('add-family-members/', add_family_members, name='add_family_member'),

    #endpoint for edit  family members 
    path('edit-family-member/<int:member_id>/', edit_family_members, name='edit_family_member'),
]

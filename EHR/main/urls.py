
from  django.urls  import path
from  main.authentication.auth import  register_user,logout_user,login_user
urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]

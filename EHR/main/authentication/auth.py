from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from models import UserProfile
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models  import  User
from  django.contrib.auth  import  login,logout,authenticate
@api_view(['POST'])
def register_user(request):
    data = request.data
    required_fields = ['name', 'email', 'gender', 'dob', 'phone_number', 'password']
    for field in required_fields:
        if not data.get(field):
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username =data['username']).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)


    user = User.objects.create(
        username=data['username'],
        email=data['email'],
        password=make_password(data['password'])
    )
    UserProfile.objects.create(
        user=user,
        dob=data.get('dob'),  # fix here
        gender=data.get('gender'),
        phone_number=data.get('phone_number')
    )

    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')  # use username
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)  # session login
        return Response({'message': 'Login successful'}, status=200)
    else:
        return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)  # ends session
    return Response({'message': 'Logged out successfully'}, status=200)


from django.views.decorators.csrf import csrf_exempt
from  rest_framework.decorators  import  api_view
from  rest_framework.response import  Response
from rest_framework import  status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction
from datetime import datetime
from ..models import FamilyMember
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

@csrf_exempt
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_family_members(request):
    data =  request.data
    required_fields  = ['username','email','dob','gender','phone_number','password']

    for fields in  required_fields:
        if not data.get(fields):
            return  Response({'message':f"required {fields} to create user"},status=status.HTTP_400_BAD_REQUEST)

    try:
        dob=  datetime.strptime(data['dob'],'%Y-%m-%d').date()

        with transaction.atomic():
            family_user=  User.objects.create(
                username = data['username'],
                email = data['email'],
                password=make_password(data['password'])
            )

            family_member = FamilyMember.objects.create(
                parent_user= request.user,
                user =  family_user,
                username=family_user.username,
                email=family_user.email,
                password=family_user.password,
                dob=dob,
                gender=data['gender'],
                phone_number= data['phone_number']
            ) 
            print('Fmaily member created',family_member)

        return  Response({'message':'Fmaily member added successfully'},status=status.HTTP_201_CREATED)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
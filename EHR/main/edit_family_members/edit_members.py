
from django.views.decorators.csrf import  csrf_exempt
from  rest_framework.decorators import  api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime
from ..models import FamilyMember
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def edit_family_members(request,member_id):

    data =  request.data
    try:
        family_member =  FamilyMember.objects.get(id=member_id,parent_user =  request.user)
        family_user =  family_member.user

        # update fields provide in the request
        if 'username' in  data:
            family_user.username =  data['username']
            family_member.username =  data['username']

        if 'email' in data:
            family_user.email =data['email']
            family_member.email =data['email']

        if  'password' in data:
            family_user.password=make_password(data['password'])
            family_member.password= family_user.password

        if 'dob' in  data:
            family_member.dob =  datetime.strptime(data['dob'],'%Y-%m-%d').date()

        if 'gender' in data:
            family_member.gender = data['gender']

        if 'phone_number' in data:
            family_member.phone_number=data['phone_number']

        family_user.save()
        family_member.save()

        return  Response({'message':'User profile is updated'},status=status.HTTP_200_OK)
    
    except FamilyMember.DoesNotExist:
        return Response({'error': 'Family member not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        # TOKEN=$(curl -s -X POST http://127.0.0.1:8000/login/ \
    #     -H "Content-Type: application/json" \
    #  -d '{"username": "subham sarkar", "password": "s123"}' | jq -r '.access')


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import FamilyMember

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])

def get_family_member_details(request,member_id):
    try:
        
        family_member =  FamilyMember.objects.get(id=member_id,parent_user=request.user)
        
        data = {
            'id':family_member.id,
            'username':family_member.username,
            'dob':family_member.dob,
            'email':family_member.email,
            'phone_number':family_member.phone_number,
            'password':family_member.password,
            'gender':family_member.gender
        }
        
        return Response(data,  status=status.HTTP_200_OK)
    
    except  FamilyMember.DoesNotExist:
        return Response({'message':'Family member does not exist  or unauthorized'},status=status.HTTP_404_NOT_FOUND)


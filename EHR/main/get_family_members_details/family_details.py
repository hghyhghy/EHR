

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import FamilyMember
from ..get_user_details.serailizers import  Familymemberserializers1
from  django.views.decorators.cache import never_cache
from  django.views.decorators.csrf import  csrf_protect

def get_all_descendants(user):

    descendants =[]
    queue = [user]

    while queue:
        
        current_user  =  queue.pop(0)
        direct_family=   FamilyMember.objects.filter(parent_user=current_user)
        descendants.extend(direct_family)
        queue.extend([member.user for member in  direct_family])
    return  descendants


@csrf_protect
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@never_cache
def get_family_member_details(request,member_id):

    user= request.user
    all_descendants =  get_all_descendants(user)
    try:
        
        family_member =  FamilyMember.objects.get(id=member_id)
        if family_member not in all_descendants:
            return  Response({'message':'Unauthorized to view this family details'},status=status.HTTP_403_FORBIDDEN)

        family_profile =  Familymemberserializers1(family_member).data
        
        return Response({
            "profile":family_profile
        },  status=status.HTTP_200_OK)
    
    except  FamilyMember.DoesNotExist:
        return Response({'message':'Family member does not exist  or unauthorized'},status=status.HTTP_404_NOT_FOUND)


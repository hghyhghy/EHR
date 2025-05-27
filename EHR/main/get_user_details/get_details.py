
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import  csrf_exempt
from ..get_user_details.serailizers import  Userprofileserializers,Familymemberserializers
from  ..models  import  UserProfile,FamilyMember



def get_all_descendends(user):
    reuslt=[]
    queue = [user]

    while queue:
        current_user = queue.pop(0)
        direct_family = FamilyMember.objects.filter(parent_user=current_user)
        reuslt.extend(direct_family)
        queue.extend([member.user for member in  direct_family])

    return reuslt

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user_profile(request):
    user =  request.user
    try:
        profile =   UserProfile.objects.get(user=user)
        profile_data =  Userprofileserializers(profile).data


        all_family =   get_all_descendends(user)
        family_data =  Familymemberserializers(all_family,many=True).data
        return  Response(
            {
                "profile":profile_data,
                'family':family_data
            }
        )

    except  UserProfile.DoesNotExist:
        return  Response({'message':'use profile is not found'},status=status.HTTP_404_NOT_FOUND)

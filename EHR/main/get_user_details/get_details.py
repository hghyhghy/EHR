
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import  csrf_exempt
from ..get_user_details.serailizers import  Userprofileserializers,Familymemberserializers
from  ..models  import  UserProfile,FamilyMember
from  django.views.decorators.csrf import  csrf_protect



def get_all_descendends(user):
    all_members =  FamilyMember.objects.select_related('user','parent_user')
    user_map={}
    for member in all_members:
        user_map.setdefault(member.parent_user_id,[]).append(member)
    reuslt=[]
    queue = [user.id]

    while queue:
        current_user = queue.pop(0)
        children  =  user_map.get(current_user,[])
        reuslt.extend(children)
        queue.extend([child.user_id for child in  children])

    return reuslt

@csrf_protect
@api_view(['GET'])
@authentication_classes([SessionAuthentication])  
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user =  request.user
    try:
        profile =   UserProfile.objects.select_related('user').get(user=user)
        profile_data =  Userprofileserializers(profile).data


        all_family =   get_all_descendends(user)
        sorted_family =  sorted(all_family,key=lambda member :  member.username.lower())
        family_data =  Familymemberserializers(sorted_family,many=True).data
        return  Response(
            {
                "profile":profile_data,
                'family':family_data
            }
        )

    except  UserProfile.DoesNotExist:
        return  Response({'message':'use profile is not found'},status=status.HTTP_404_NOT_FOUND)

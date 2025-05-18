
from rest_framework import  serializers
from  ..models import  UserProfile,FamilyMember


class Userprofileserializers(serializers.ModelSerializer):
    class Meta:
        model =  UserProfile
        fields = ['username','email','dob','gender','phone_number','password']

    
class  Familymemberserializers(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = ['username','email','dob','gender','phone_number','password']


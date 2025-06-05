
from rest_framework import  serializers
from  ..models import  UserProfile,FamilyMember
from django.core import  signing

class Userprofileserializers(serializers.ModelSerializer):
    
    class Meta:
        model =  UserProfile
        fields = [ 'id','username','email','dob','gender','phone_number','password']

    
class  Familymemberserializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    class Meta:
        model = FamilyMember
        fields = [ 'uuid','id','user_id','username','email','dob','gender','phone_number','password']
        
class  Familymemberserializers1(serializers.ModelSerializer):

    
    class Meta:
        model = FamilyMember
        fields = [ 'uuid','username','email','dob','gender','phone_number']


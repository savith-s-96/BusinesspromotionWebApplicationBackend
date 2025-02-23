from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


class RegisterSerializer(ModelSerializer):


       class Meta:
              
               model = get_user_model()
               fields = ["username","id","date_joined","password"]
               extra_kwargs = {"password" : {"write_only" : True}}

        
       def validate(self, attrs):
          
             return attrs
       
       def create(self, validated_data):
               
    
               user = get_user_model().objects.create_user(username=validated_data["username"])
               user.set_password(validated_data["password"])
               user.save()
               return user
              
       
       def update_password(self, instance, userpassword):
              
              instance.change_password(userpassword)
              instance.save()
              return instance        

       def update_username(self, instance, username):
              
              instance.username = username
              instance.save()               
              return instance


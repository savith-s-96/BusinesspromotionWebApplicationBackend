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
              
       
       def update_password(self, instance, userpassword = None):
              
              if(userpassword and len(userpassword) >= 8 ):

                instance.set_password(userpassword)
                instance.save()
                return instance 
              
              else:

                    return None       

       def update_username(self, instance, username = None):
              
              if(username and username.isalnum()):
                
                try: 
                
                 instance.username = username
                 instance.save()               
                 return instance
                
                except Exception:
              
                   return None
               
              else:
                    
                  return None


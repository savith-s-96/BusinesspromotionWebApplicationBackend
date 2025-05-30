from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField
from django.contrib.auth import get_user_model
from Models.models import Profile, Address, SocialMedia, Posts, Products

class RegisterSerializer(ModelSerializer):


       class Meta:
              
               model = get_user_model()
               fields = ["username","id","date_joined","password"]
               extra_kwargs = {"password" : {"write_only" : True,}}

        
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
              




class AddressSerializer(ModelSerializer) :
     
     class Meta :
          
          model = Address
          fields = '__all__'

     def create(self, validated_data):
          

          return Address.objects.create(**validated_data)
     
     def update(self,instance,validated_data) :

          address_filter_query = Address.objects.filter( id = instance.id)
          address_filter_query.update(**validated_data)
          return address_filter_query[0]



class SocialMediaSerializer(ModelSerializer) :
     

     class Meta :
          
          model = SocialMedia 
          fields = "__all__"


     def create(self,validated_data) :
           
           
           return SocialMedia.objects.create(**validated_data)

          
          
     
     def update(self, instance, validated_data):
          
           socialMedia_filter_query = SocialMedia.objects.filter( id =  instance.id)
           socialMedia_filter_query.update(**validated_data)
           return socialMedia_filter_query[0]


class ProfileSerializer(ModelSerializer) :
     
      address = PrimaryKeyRelatedField(queryset=Address.objects.all(), required=True)
      socialMedia = PrimaryKeyRelatedField(queryset=SocialMedia.objects.all(), required=True)
      class Meta :
           
            model = Profile
            fields = ['user','shop_name','profile_image_url','mobile_number','slogan','socialMedia','address','created_at','last_updated_at']
            
            
      def __init__(self,*args,**kwargs) :
            
            self.exclude_feilds = kwargs.pop("exclude_feilds",[])
            super().__init__(*args,**kwargs)

            for exclude_feild in self.exclude_feilds :
                  
                  self.fields.pop(exclude_feild,None)

      def create(self, validated_data):
           
           return Profile.objects.create(**validated_data)

      def update(self,instance,validated_data) :
     
           profile_filer_query = Profile.objects.filter(user = instance.user)
           profile_filer_query.update(**validated_data)

           return profile_filer_query[0]
            
           
class PostSerializer(ModelSerializer) :

            
            user = PrimaryKeyRelatedField(queryset = Posts.objects.all())

            class Meta :
                 
                 model = Posts 
                 fields = "__all__"
                 read_only_fields = ["user","post_type","post_url","post_description","thumbnail_url","uploaded_at"]

class ProductSerializer(ModelSerializer) :

           user = PrimaryKeyRelatedField(queryset = Products.objects.all())
          
           class Meta :
                 
                 model = Products
                 fields = "__all__"
                 read_only_fields = ["user","product_image_url","product_name","product_prize","created_at"]
           
      
from django.db import models
from django.contrib.auth import get_user_model

     
class SocialMedia(models.Model) :
     
     instagram = models.URLField(null=True,blank=True)
     linked_in = models.URLField(null=True,blank=True)
     youtupe = models.URLField(null=True,blank=True)
     whatshap = models.IntegerField(null=False,blank=False)
     email = models.EmailField(null=True,blank=True)


class Address(models.Model) :
     

     street = models.CharField(max_length=200,null=False,blank=False)
     city = models.CharField(max_length=100,null=False,blank=False)
     district = models.CharField(max_length=100,null=False,blank=False)
     pincode = models.IntegerField(null=False,blank=False)
     state = models.CharField(max_length=100,null=False,blank=False)
     country = models.CharField(max_length=100,null=False,blank=False)
     google_map_link = models.URLField(null=False,blank=False)

class Profile(models.Model) :


     user = models.OneToOneField(get_user_model(), related_name='user_profile',on_delete=models.CASCADE,primary_key=True)
     shop_name = models.CharField(max_length=200,default='noob',null=False,blank=False)
     profile_image_url = models.URLField(null=True) 
     mobile_number = models.CharField(max_length=15,null=False)
     slogan = models.TextField(null=True,blank=True)
     socialMedia = models.OneToOneField(SocialMedia,related_name='social_profile',on_delete=models.CASCADE,null=False)
     address = models.OneToOneField(Address,related_name='address_profile',on_delete=models.CASCADE,null=False)
     created_at = models.DateTimeField(auto_now_add=True)
     last_updated_at = models.DateTimeField(auto_now=True)



class Posts(models.Model) :

      user = models.ForeignKey(get_user_model(),related_name="posts",on_delete=models.CASCADE)
      post_type = models.CharField(max_length=100)
      post_url = models.URLField()
      post_description = models.TextField(null=True)
      thumbnail_url = models.URLField(null=True)
      uploaded_at = models.DateTimeField(auto_now_add=True)

class Products(models.Model) :


     user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
     product_image_url = models.TextField(null=False,blank=False)
     product_name = models.CharField(max_length=50,null=False,blank=False)
     product_prize = models.IntegerField(null=False,blank=False)
     created_at = models.DateTimeField(auto_now_add=True,null=False)

def get_or_none(model,**kwargs) :

      
      try :
           
           object = model.objects.get(**kwargs)
           return object
      
      except Exception as e :
           
           print(e)
           return None
      


def filter_or_none(model,**kwargs) :

     objects = model.objects.filter(**kwargs)

     if(len(objects)) :

          return objects
     
     else :

          return None




       
     



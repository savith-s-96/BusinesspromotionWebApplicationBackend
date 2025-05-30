try :
      from rest_framework.views import APIView
      from rest_framework.response import Response
      from rest_framework.request import Request
      from Serializers.Serializers import RegisterSerializer, AddressSerializer, ProfileSerializer, SocialMediaSerializer,PostSerializer,ProductSerializer
      from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
      from rest_framework.permissions import IsAuthenticated
      from django.contrib.auth import get_user_model
      # from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
      from rest_framework_simplejwt.tokens import RefreshToken
#     from Locito.settings import SIMPLE_JWT
      # from datetime import timedelta, datetime, timezone
      from Models.models import Profile,Address,SocialMedia,get_or_none,Posts,Products,filter_or_none
      # from django.shortcuts import redirect
      # from django.urls import reverse
      import time
      # import jwt
      from django.conf import settings
      # import time

except ImportError as error :

       print("Import Error : ",error.name)
       import sys 
       sys.exit()


class RegisterView(APIView):


   
     def post(self,request) -> Response :
               
              data = request.data 

              if(len(data) == 2 and "username" in data and "password" in data and len(data["password"]) >= 8 and data["username"].isalnum()):
                 serializer = RegisterSerializer(data=data)
                 if(serializer.is_valid()):
                     
                      user = serializer.save()
                      return Response({"message" : "success"},status=200)
              
                 else:
                     
                     return Response({"message" : "username already exists"},status=400)
              else:
                   
                   return Response({"message" : "invalid credentials"},status=400)

class UpdateUsername(APIView):
       
       
       permission_classes = [IsAuthenticated]
       authentication_classes = [JWTTokenUserAuthentication]
       
       def put(self,request) -> Response :
              

              data = request.data 
            #   print(request.META["HTTP_AUTHORIZATION"])
              if(len(data) == 2 and "username" in data and "user_id" in data):
               
                
                     
                user = get_or_none(get_user_model(),id = data.get("user_id"))
               
             
                if(user):
                     
                      serializer = RegisterSerializer().update_username(instance = user,username = data["username"])
                      
                      if(serializer):
                      
                            return Response({"message" : "success","userid" : serializer.id},200)
                      
                      else:

                            return Response({"message ":"username invalid"},status=401)
                else:
                    
                     return Response({"message" : "invalid userid"},status=401)
                
              else:
                    
                    return Response({"message" : "invalid credentials"},status=401)
              


class UpdatePassword(APIView):
      
      permission_classes = [IsAuthenticated]
      authentication_classes = [JWTTokenUserAuthentication]
      
      def put(self,request) -> Response :

                 data = request.data
                 if(len(data) == 2 and "user_id" in data and "password" in data and len(data["password"]) >= 8):
                  
                    
                   
                    user = get_or_none(get_user_model(),id = data.get("user_id"))
                 

                 
                    if(user) :

                        serializer = RegisterSerializer().update_password(instance = user, userpassword = data["password"])
                        
                        if(serializer):
                    
                            return Response({"message":"success","userid" : serializer.id },status=200)
                     
                        else:
                             
                            return Response({"message" : "invalid password"},status=401)
                    else:

                         return Response({"message" : "invalid userid"},status=401)
              
                 else:
                       
                        return Response({"message" : "invalid credentials"},status=401)
                 


class customTokenObtainPairView(APIView) :
     

           def post(self,request) -> Response :
                 
                   data = request.data
                   userModel = get_user_model()
                   try :
                     user = userModel.objects.get(username = data["username"])
                  #    print(user)
                  #    print(user.id)
                     if(user) :
                         
                         if(user.check_password(data["password"])) :
                               
                                 token = RefreshToken.for_user(user)
            
                                 response = Response({"message" : "success","userId" : user.id,"refreshToken" : str(token),"accessToken" : str(token.access_token),},status=200)

                                 return response
                         else :
                               
                               return Response({"message" : "invalid password"},status=401)
           
                     else :
                         

                         return Response({"message" : "invalid user credentials"},status=401)
                   except Exception as e :

                         print(e)         
                        
                         return Response({"message" : "user does not exist"},status=401)    

class AccessToken(APIView) :

      def get(self,request) :
      
           refresh_token = request.GET.get("refreshToken",None)
           if(refresh_token) :

                  token =  RefreshToken(refresh_token)
                  access_token = token.access_token
                  response = Response({"message" : "succesful", "accessToken" : str(access_token),"userId" : str(access_token["user_id"])},status=200)

                  return response

           else :
                 print(refresh_token)
                 return Response({"message : invaild refreshtoken"},status=401)     




class CreateProfile(APIView) :

    
       permission_classes = [IsAuthenticated]
       authentication_classes = [JWTTokenUserAuthentication]

       def post(self,request : Request) :


               data = request.data 
            #    print(data)
            #    print(data)
               user_id = data.get("user_id",None)
               if(user_id) :
                     
                  try :
                     
                     user = get_user_model().objects.get(id = user_id)
                     address_data = data.get("address_data",None)
                     social_media_data = data.get("social_media_data",None)
                     profile_data = data.get("profile_data",None)
                     if(not get_or_none(model=Profile,user = user)) :
                           
                           if(address_data and social_media_data and profile_data) :
                                 
                                 address_serializer = AddressSerializer(data = address_data)
                                 social_media_serializer = SocialMediaSerializer(data = social_media_data)
                                 if(social_media_serializer.is_valid(raise_exception=True) and address_serializer.is_valid(raise_exception=True)) :
                                       
                                     social_media =  social_media_serializer.save()
                                     address = address_serializer.save()
                                     profile_data["address"] = address.id
                                     profile_data["socialMedia"] = social_media.id
                                     profile_data["user"] = user.id
                                     profile_serializer = ProfileSerializer(data = profile_data)

                                     if(profile_serializer.is_valid(raise_exception=True)) :
                                           

                                          #   profile = profile_serializer.save()
                                            profile_serializer.save()
                                            return Response({"message" : "success"},status=200)

                           
                           else :
                                 
                                 return Response({"message" : "invalid data"},status=401)
                     
                     else :
                           
                                 profile = Profile.objects.get(user = user)

                                 if(address_data) :
                                       address = Address.objects.get( id = profile.address.id)
                                       address = AddressSerializer(address,data = address_data,partial = True)
                                       if(address.is_valid()) :
                                             
                                             address.save()

                                       else :
                                             
                                             return Response({"message" : "invalid address data"},status=401)
                                       
                                 if(social_media_data) :
                                       
                                        social_media = SocialMedia.objects.get( id = profile.socialMedia.id)
                                        social_media = SocialMediaSerializer(social_media,data = social_media_data,partial=True)
                                        if(social_media.is_valid()) :
                                              
                                               social_media.save()
                                        else :
                                              
                                              print(social_media.errors)
                                              return Response({"message" : "invalid social Media data"},status=401)
                                        
                                 if(profile_data) :
                                       
                                       profile = ProfileSerializer(profile,data = profile_data,partial = True)
                                       if(profile.is_valid()) :
                                            
                                              profile.save()
                                              
                                       else :
                                             
                                             
                                             return Response({"message" : "profile invalid data"},status=401)
                                 profile = Profile.objects.get(user = user)
                                 profile = ProfileSerializer(profile)
                                 data = profile.data
                                 return Response({"message" : "success","data" : data},status=200)
                       

                  except Exception as e :

                      
                        return Response({"message" : str(e)},status=401)

                     
               
               else :
                     
                     return Response({"message" : "user id missing"},status=401)
               



class getProfile(APIView) :


      permission_classes = [IsAuthenticated]
      authentication_classes = [JWTTokenUserAuthentication]

      def get(self,request) :


            user_id = request.GET.get("user_id",None)
            print("requsets received")
            if(user_id) :

                  user = get_or_none(get_user_model(),id = user_id)

                  if(user) :

                        profile = get_or_none(Profile,user = user)
                        if(profile) :

                              data = ProfileSerializer(profile).data
                              data["username"] = RegisterSerializer(user).data["username"]
                              address = Address.objects.get(id = data["address"])
                              socialMedia = SocialMedia.objects.get(id = data["socialMedia"])
                              data["address"] = AddressSerializer(address).data
                              data["socialMedia"] = SocialMediaSerializer(socialMedia).data
                              data["message"] = "succcess"
                              data['profile'] = True
                              return Response({"data" : data},status=200)

                        else :

                               data = {'message' : "Profile does not exist",'profile' : False}
                               return Response({"data" : data},status=400)

                  else :


                        return Response({"message" : "user is not registerd"},status=400)

            else :

                  return Response({"message" : 'user id is invalid'},status=400)


               
class getPosts(APIView) :


      permission_classes = [IsAuthenticated]
      authentication_classes = [JWTTokenUserAuthentication]


      def get(self,request) :


            page_no = int(request.GET.get("page",None))
            user_id = request.GET.get("user_id",None)
            page_size = 10
            print(page_no)
            print(user_id)
            if(page_no and user_id and len(request.GET) == 2) :
                            
                            page_no = page_no - 1
                            user = get_or_none(get_user_model(),id = user_id)
                            if(user) :
                                  
                                  posts = Posts.objects.filter(user = user).order_by("-uploaded_at")[page_no * page_size : (page_no * page_size) + page_size]
                              #     print(posts[0].post_url)

                                  if(len(posts)>=1) :
                                        
                                        try :
                                         
                                          post_serializer = PostSerializer(posts,many=True) 
                                          time.sleep(1)
                                          return Response(post_serializer.data,status = 200)
                                        
                                        except Exception as e :
                                              
                                              return Response({"message" : str(e)},status=401)
                                        
                                  
                                  else :
                                        time.sleep(1)
                                        return Response({"message" : "No more data "},status=200)

                            
                            else :
                                  
                                  return Response({"message" : "user missing"},status=401)
               

            else :

                  return Response({"message" : "invalid query parameters"},status=401)


class getProfileImageUrl(APIView) :


      permission_classes = [IsAuthenticated]
      authentication_classes = [JWTTokenUserAuthentication]

      def get(self,request) :


            user_id = request.GET.get("user_id",None)

            if(user_id) :

                  user = get_or_none(get_user_model(),id = user_id)

                  if(user) :

                        profile = get_or_none(Profile,user = user)

                        if(profile) :

                              return Response({"profileImageUrl" : profile.profile_image_url,"profileName" : profile.shop_name},status=200)

                        else :

                              return Response({"message" : "profile not created"},status=401)

                  else :


                        return Response({"message" : "user not registered"},status=401)

            else  :


                  return Response({"message" : "invalid"},status=401)
            



               
class getProducts(APIView) :


      permission_classes = [IsAuthenticated]
      authentication_classes = [JWTTokenUserAuthentication]


      def get(self,request) :

   
            page_no = int(request.GET.get("page",None))
            user_id = request.GET.get("user_id",None)
            page_size = 10
            print(page_no)
            print(user_id)
            if(page_no and user_id and len(request.GET) == 2) :
                           try : 
                             
                             page_no = page_no - 1
                             user = get_or_none(get_user_model(),id = user_id)
                             if(user) :
                                  
                                  products = Products.objects.filter(user = user).order_by("-created_at")[page_no * page_size : (page_no * page_size) + page_size]
                              #     print(posts[0].post_url)
                                  print(products)
                                  if(len(products)>=1) :
                                        
                                        try :
                                         
                                          product_serializer = ProductSerializer(products,many = True)
                                          time.sleep(1)
                                          return Response(product_serializer.data,status = 200)
                                        
                                        except Exception as e :
                                              
                                              return Response({"message" : str(e)},status=401)
                                        
                                  
                                  else :
                                        time.sleep(1)
                                        return Response({"message" : "No more data "},status=200)

                            
                             else :
                                  
                                  return Response({"message" : "user missing"},status=401)
                             
                           except Exception as e:
                                 
                                  return Response({"message" : "invalid query parameters"},status=401)
            else :

                  return Response({"message" : "invalid query parameters"},status=401)
            


class SearchProfile(APIView) :


      def get(self,request) :

            cityName = request.GET.get("cityName",None)

            if(cityName) :
                 
                 print("cityName", cityName)
                 address_objects = filter_or_none(Address,city = cityName)
                 print("address objects",address_objects)
                 if(address_objects) :
                       
                       profiles = []
                       try :
                             
                         for address_object in address_objects :
                             
                             profiles.append(address_object.address_profile)
                  
                         print(profiles)

                       except Exception as e:
                             
                             print(e)
                             time.sleep(2)
                             return Response({"message" : "Not Found"},status=200)
                       
                       serialized_profile_object = ProfileSerializer(profiles,exclude_feilds = ['mobile_number','slogan','socialMedia','address','created_at','last_updated_at'],many = True)
                       time.sleep(2)
                       return Response({"message" : "success","data" : serialized_profile_object.data},status=200)

                 
                 else :
                       time.sleep(2)
                       return Response({"message" : "Not Found"},status=200)


            else :

                  return Response({"message" : "invalid search query"},status=401)
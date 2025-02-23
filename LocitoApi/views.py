from rest_framework.views import APIView
from rest_framework.response import Response
from Serializers.Serializers import RegisterSerializer
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model




class RegisterView(APIView):



     def post(self,request) -> Response :
          
              data = request.data 
              if(len(data) == 2 and "username" in data and "password" in data and len(data["password"]) >= 8 and data["username"].isalnum()):
                 serializer = RegisterSerializer(data=data)
                 if(serializer.is_valid()):
                     
                      serializer.save()
                      return Response({"message" : "success"},status=200)
              
                 else:
                     
                     return Response({"message" : "username already exists"},status=400)
              else:
                   
                   return Response({"message" : "invalid credentials"},status=401)

class UpdateUsername(APIView):

       permission_classes = [IsAuthenticated]
       authentication_classes = [JWTTokenUserAuthentication]
       
       def put(self,request) -> Response :
              

              data = request.data 
              if(len(data) == 2 and "username" in data and "id" in data):
               
                try:
                     
                      user = get_user_model().objects.get(id = data["id"])
               
                except KeyError:

                      return Response({"message" : "userid Missing"},status=401)
                    
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
                 if(len(data) == 2 and "id" in data and "password" in data and len(data["password"]) >= 8):
                  
                    try:
                   
                       user = get_user_model().objects.get(id = data["id"])
                 
                    except KeyError:

                       return Response({"message" : "userid Missing"},status=401)
                 
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
from rest_framework.views import APIView
from rest_framework.response import Response
from Serializers.Serializers import RegisterSerializer
from django.contrib.auth import get_user_model




class RegisterView(APIView):



     def post(self,request) -> Response :
          
              data = request.data 
              serializer = RegisterSerializer(data=data)
              if(serializer.is_valid()):
                     
                      serializer.save()
                      return Response({"message" : "success"},status=200)
              
              else:
                     
                     return Response({"message" : "username already exists"},status=400)


class UpdateUsername(APIView):
       
       def put(self,request) -> Response :
              

              data = request.data 
              user = get_user_model().objects.get(id = data["userid"])
              if(user):
              
                RegisterSerializer().update_username(instance = user,username = data["username"])
                return Response({"message" : "success"},200)

              else:
                    
                    return Response({"message" : "invalid userid"},status=401)
              


class UpdatePassword(APIView):
      

      def put(self,request) -> Response :

                 data = request.data
                 user = get_user_model().objects.get(id = data["userid"])

                 if(user) :

                        RegisterSerializer().update_password(instance=user,validated_data=data["password"])

                        return Response({"message":"success"},status=200)
                 
                 else:

                        return Response({"message" : "invalid userid"},status=401)
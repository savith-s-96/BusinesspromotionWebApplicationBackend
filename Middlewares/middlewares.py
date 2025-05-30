from rest_framework_simplejwt.tokens import RefreshToken
class AuthorizationMiddleWare :



        def __init__(self,get_response):
                
                self.get_response = get_response

            
        def __call__(self, request):
                
               print(request.COOKIES) 
               access_token = request.COOKIES.get("access")
               if(access_token) :
                       
                        request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
        
               response = self.get_response(request)  
               return response 
        
       

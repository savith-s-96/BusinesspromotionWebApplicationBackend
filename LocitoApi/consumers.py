from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from pathlib import Path
from os import path
import aiofiles
from Models.models import Posts,Products,Profile
from django.contrib.auth import get_user_model
from datetime import datetime
import os 
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Locito.settings')



Base_dir = Path(__file__).parent.parent
post_media_dir = path.join(Base_dir,"media","posts")
thumnail_media_dir = path.join(Base_dir,"media","thumbnail_images")
product_media_dir = path.join(Base_dir,"media","product_images")
profile_media_dir = path.join(Base_dir,"media","profile_images")


async def get_or_none(model,**feilds) :
       
        try :
               
               return await model.objects.aget(**feilds)
        except Exception as e :

             print(e)
             return None
        

@sync_to_async
def save_instance(instance) :
       
       instance.save()

class PostUpload(AsyncWebsocketConsumer) :

        async def connect(self):
                
                await self.accept()
                await self.send(text_data="post upload starting....")
                raw_query_params = self.scope["query_string"] 
                self.query_params = parse_qs(raw_query_params.decode())
                print(self.query_params.get("post_file_name"))
                self.post_file_name = path.join(post_media_dir,self.query_params.get("post_file_name")[0])
                self.post_file_size = int(self.query_params.get("post_file_size")[0])
                self.post_file_object = await aiofiles.open(self.post_file_name,"ab")
                self.thumbnail_file_name = path.join(thumnail_media_dir,self.query_params.get("thumbnail_file_name")[0])
                self.thumbnail_file_size = int(self.query_params.get("thumbnail_file_size")[0])
                self.thumbnail_file_object = await aiofiles.open(self.thumbnail_file_name,"ab")
                self.file_size = self.post_file_size
                self.file = self.post_file_object 
                self.received_bytes = 0 
                self.post_url = path.join("media","posts",self.query_params.get("post_file_name")[0])
                self.thumbnail_url = path.join("media","thumbnail_images",self.query_params.get("thumbnail_file_name")[0])
                self.user_id = self.query_params.get("user_id")[0]
                self.post_description = self.query_params.get("post_description")[0]
                self.post_file_type = self.query_params.get("post_file_type")[0]
                

        async def receive(self, text_data=None, bytes_data=None):
                
                if(bytes_data) :
                        
                     await self.file.write(bytes_data)
                     self.received_bytes = self.received_bytes + len(bytes_data)

                     if(self.received_bytes >= self.file_size) :
                            
                            if(self.file == self.post_file_object) :
                                   
                                   self.received_bytes = 0
                                   self.file = self.thumbnail_file_object
                                   self.file_size = self.thumbnail_file_size
                            else :
                                   
                                   if(self.file == self.thumbnail_file_object and self.received_bytes >= self.thumbnail_file_size) :
                                           
                                            #  print(self.user_id)
                                             user = await get_or_none(get_user_model(),id = self.user_id)
                                             print("user : " , user)
                                             if(user) :
                                                    
                                                  if(self.post_description and self.post_description!="undefined") :
                                                         print("post updated in database")
                                                         Post = Posts(user_id = self.user_id, post_type = self.post_file_type, post_url = self.post_url, thumbnail_url = self.thumbnail_url,post_description = self.post_description, uploaded_at = datetime.now()) 
                                                         await save_instance(Post)
                                                  else :
                                                        
                                                         Post = Posts(user_id = self.user_id, post_type = self.post_file_type, post_url = self.post_url, thumbnail_url = self.thumbnail_url, uploaded_at = datetime.now())
                                                         print("post : ",Post)
                                                         print("post url : ", self.post_url)
                                                         print("thumbnail_url : ",self.thumbnail_url)
                                                         await save_instance(Post)
                                             
                                                    
                                             await self.close()
                               

                
        async def disconnect(self, code):
                
                print("websocket connection closed")
        

                        
class ProductUpload(AsyncWebsocketConsumer) :

       async def connect(self):
              
              await self.accept()
              await self.send(text_data="websocket connection open")
              self.query_params = parse_qs(self.scope["query_string"].decode())
              self.file_name = path.join(product_media_dir,self.query_params.get("file_name")[0])
              self.file_object = await aiofiles.open(self.file_name,"ab")
              self.file_size = int(self.query_params.get("file_size")[0])
              self.product_url = os.path.join("media","product_images",self.query_params.get("file_name")[0])
              self.bytes_received = 0

       
       async def receive(self, text_data=None, bytes_data=None):
              
              if(bytes_data) :

                     await self.file_object.write(bytes_data)
                     self.bytes_received = self.bytes_received + len(bytes_data)

                     if(self.bytes_received >= self.file_size) :

                            user = await get_or_none(get_user_model(),id = self.query_params.get("user_id")[0])
                            if(user) :
                               product = Products(user = user, product_image_url = self.product_url, product_name = self.query_params.get("product_name")[0], product_prize = self.query_params.get("product_prize")[0])
                               await save_instance(product)
                               await self.close()



class ProfileImageUpload(AsyncWebsocketConsumer) :


          async def connect(self):
                 
                 await self.accept()
                 await self.send(text_data="websocket connection open")
                 self.query_params = parse_qs(self.scope["query_string"].decode())
                 self.file_name = path.join(profile_media_dir,self.query_params.get("file_name")[0])
                 self.file_size = int(self.query_params.get("file_size")[0])
                 self.bytes_received = 0
                 self.profile_image_url = path.join("media","profile_images",self.query_params.get("file_name")[0])
                 self.file_object = await aiofiles.open(self.file_name,"ab")

          async def receive(self, text_data=None, bytes_data=None):
                 
                 if(bytes_data) :
                        
                        await self.file_object.write(bytes_data)
                        self.bytes_received = self.bytes_received + len(bytes_data)

                        if(self.bytes_received >= self.file_size) :
                               
                                user = await get_or_none(get_user_model(), id = self.query_params.get("user_id")[0])

                                if(user) :
                                       
                                     profile = await get_or_none(Profile, user = user)

                                     if(profile) :

                                            profile.profile_image_url = self.profile_image_url

                                            await save_instance(profile) 

                                     await self.close()  
                         
       
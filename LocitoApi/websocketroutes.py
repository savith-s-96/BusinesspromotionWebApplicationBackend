from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
   re_path(r"ws/upload-posts/?$",consumers.PostUpload.as_asgi()),
   re_path(r"ws/uploadProduct/?$",consumers.ProductUpload.as_asgi()),
   re_path(r"ws/profile-image-upload/?$",consumers.ProfileImageUpload.as_asgi()),

]
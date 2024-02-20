
from django.contrib import admin
from django.urls import path
from gmap.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_file, name='upload'),
    path('',signin,name='login'),
    path('signup/',signup,name='signup'),
    path('home/',home, name='home'),
    path('map/',show_location,name='map'),
    path('leads/', show_leads, name='leads'),
    path("logout/",signout,name="logout"),
    path('profile/',profile, name='profile'),
    path('forgot/',forgot,name="forgot")
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tres_coelhos.urls')), 
    path('', include('sky_view.urls')), 
    path('', include('gran_vitta.urls')), 
    path('', include('passaros.urls')), 

]




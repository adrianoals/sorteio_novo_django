from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tres_coelhos.urls')), 
    path('', include('sky_view.urls')), 
    path('', include('gran_vitta.urls')), 
    path('', include('passaros.urls')), 
    path('', include('ventura.urls')), 
    path('', include('arthur.urls')), 
    path('', include('alvorada.urls')), 
    path('', include('splendore.urls')),
    path('', include('helborsorteio.urls')),
]




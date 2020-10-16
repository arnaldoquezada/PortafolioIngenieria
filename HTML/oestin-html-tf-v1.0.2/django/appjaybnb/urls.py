from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static
from .views import home, team, contacto, successView, roomGrid

urlpatterns = [
    path('', home, name='home'),
    path('propiedades/todas/', roomGrid, name='roomgrid'),
    path('info/team/', team, name='team'),
    path('info/contacto/', contacto, name='contacto'),
    path('info/contacto/', successView, name='success'),
    path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
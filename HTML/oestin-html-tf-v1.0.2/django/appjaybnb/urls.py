from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static
from .views import home, team, contacto, successView, roomGrid, detallePropiedad, perfil, register, Pago, reservaexito

urlpatterns = [
    path('', home, name='home'),
    path('propiedades/todas/', roomGrid, name='roomgrid'),
    path('propiedades/detalle/<str:pk>', detallePropiedad, name='roomdetail'),
    path('cliente/perfil/', perfil, name='perfil'),
    path('info/team/', team, name='team'),
    path('reserva/exito/', reservaexito, name='rexito'),
    path('pagos/formas/', Pago, name='pago'),
    path('info/contacto/', contacto, name='contacto'),
    path('info/contacto/', successView, name='success'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', register, name='signup'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
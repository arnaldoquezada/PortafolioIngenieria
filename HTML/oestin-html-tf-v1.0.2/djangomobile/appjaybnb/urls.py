from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static
from .views import home, team, contacto, successView, roomGrid, detallePropiedad, perfil, register, Pago, reservaexito, preRoomDetail, busqueda, resubusqueda, checkinOk, checkindatos, aceptaCheckin, busqueda_out, aceptaCheckOut, checkOutOk

urlpatterns = [
    path('', home, name='home'),
    path('propiedades/todas/', roomGrid, name='roomgrid'),
    path('propiedades/detalle/<str:pk>', detallePropiedad, name='roomdetail'),
    path('propiedades/predetalle/<int:pk>', preRoomDetail, name='preroomdetail'),
    path('cliente/perfil/', perfil, name='perfil'),
    path('reserva/busqueda/', busqueda, name='busqueda'),
    path('reserva/busqueda_out/', busqueda_out, name='busqueda_out'),
    path('reserva/resubusqueda/', resubusqueda, name='resubusqueda'),
    path('reserva/checkinok/', checkinOk, name='checkinok'),
    path('reserva/checkindatos/<str:pk>', checkindatos, name='checkindatos'),
    path('reserva/aceptaCheckin/<str:pk>', aceptaCheckin, name='aceptacheckin'),
    path('reserva/aceptaCheckOut/<str:pk>', aceptaCheckOut, name='aceptacheckout'),
    path('reserva/checkoutok/', checkOutOk, name='checkoutok'),
    path('info/team/', team, name='team'),
    path('reserva/exito/', reservaexito, name='rexito'),
    path('signup/', register, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

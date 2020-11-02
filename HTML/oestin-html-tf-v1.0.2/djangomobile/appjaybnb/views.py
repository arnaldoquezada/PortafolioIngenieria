from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q, Count
from datetime import datetime
from dateutil.parser import parse
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse_lazy
from django.views import generic
import cx_Oracle
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django_group_by import GroupByMixin
from .models import Imagen, Propiedad, Cliente, Comuna, AuthUser, EstadoCli, Region, Reserva, Propiedades, EstadoReserv, DetallePropiedad, CheckIn, CheckList
from datetime import date
from django.core.validators import RegexValidator

#conexion base de datos
conn = cx_Oracle.connect("jaybnb","jaybnb","localhost/XE", encoding="UTF-8")

def register(request):

    if request.method == "POST":
        print("Es POST")
        rut = request.POST["run"]
        nombre = request.POST["nombre"]
        apepaterno = request.POST["apepaterno"]
        apematerno = request.POST["apematerno"]
        fechanac = request.POST["fechanac"]
        email = request.POST["email"]
        direccion = request.POST["direccion"]
        fono = request.POST["telefono"]
        estado = 'S'
        #idcomuna = request.POST.get("comuna")

        idestadocli = EstadoCli.objects.get(id_estado_clie=1)
        print(idestadocli.id_estado_clie)
        #idestado = EstadoCli()
        #idestado.id_estado_clie = idestadocli.id_estado_clie
        idcomuna = Comuna.objects.get(id_comuna=1)
        print(idcomuna.id_comuna)
        #idcom = idcomuna.id_comuna
        passw = request.POST["password"]

        user = User.objects.create_user(username=email, email=email, password=passw, first_name='C')
        user.save()

        id_cliente = AuthUser.objects.latest('id')

        cliente_datos = Cliente(id_cliente=id_cliente.id, rut=rut, nombres_clien=nombre, apellido_p=apepaterno, apellido_m=apematerno, fecha_nac=fechanac, email=email, direccion=direccion, telefono=fono, estado=estado, id_estado_clie=idestadocli, id_comuna=idcomuna, password=id_cliente.password )
        cliente_datos.save()

        return redirect('login')
    else:
        comuna = Comuna.objects.all()

    return render(request, 'registration/signup.html', {'comuna': comuna})

# Create your views here.
class ContactForm(object):
    from_email = ""
    subject = ""
    message = ""

class Idprop(object):
    id_propiedad = []

@login_required
def home(request):
    return render(request, 'movil/mainmenu.html')

@login_required
def busqueda(request):
    if request.method == "POST":
        print("Es POST")
        idp = request.POST["idpropiedad"]
        if not idp.isdigit():
            idp = 0
        try:
            idprop = Propiedad.objects.get(id_propiedad=idp)
            idestadores = EstadoReserv.objects.get(id_estado_rese=2)
            res = Reserva.objects.filter(id_propiedad=idprop.id_propiedad, id_estado_rese=idestadores)
            return render(request, 'movil/result_busqueda.html', {'res':res})
        except Propiedad.DoesNotExist as den:
            print(den)
            sinres = 0
            return render(request, 'movil/result_busqueda.html', {'sinres':sinres})
    else:
        comuna = Comuna.objects.all()
    return render(request, 'movil/busqueda.html')

@login_required
def resubusqueda(request):
    return render(request, 'movil/result_busqueda.html')

@login_required
def checkindatos(request, pk):
    if request.method == "POST":
        print("Checkin Datos PK"+pk)
        res = Reserva.objects.get(id_reserva=pk);
        return render(request, 'movil/aceptacion_in.html',{'res':res})
    else:
        prop = Propiedad.objects.all()
    return render(request, 'movil/check-in_datos_arrendatario.html',{'prop': prop})

@login_required
def aceptaCheckin(request, pk):
    res = Reserva.objects.get(id_reserva=pk)
    print(res.id_cliente.nombres_clien)
    if request.method == "POST":
        idres = request.POST["idreserva"]
        print("Print Acepta POST id reserva "+idres)
        estadores = EstadoReserv.objects.get(id_estado_rese=3)
        print(estadores)
        rese = Reserva.objects.get(id_reserva=idres)
        rese.id_estado_rese = estadores
        rese.save()

        now = datetime.now()


        try:
            # create a connection to the Oracle Database
            #connection = cx_Oracle.connect("hr", userpwd, "dbhost.example.com/orclpdb1", encoding="UTF-8")

            cur = conn.cursor()
            cur.callproc('sp_crear_checkin', (now, "S", res.id_reserva))


        except Exception as errr:
            print("error: ", errr)
        else:
            try:
                #cur.callproc('pkg_reservas.sp_crear_reserva', (fechaini, fechafin, cantidad, idpropiedad, idcliente))
                print("Pasó por aquí?")
            except:
                print("No funciono")
            else:
                print("Funciono el procedimiento")
                return redirect('checkinok')

            finally:
                print("Cerrando Conexión")
                cur.close()
        finally:
            print("Termino el proceso")

        #check = CheckIn(id_check_list=s_checklist.nextvalue, fecha_check=now, acepta_termino="S", id_reserva=res)
        #check.save()
    else:
        prop = Propiedad.objects.all()
        return render(request, 'movil/aceptacion_in.html',{'res':res})

@login_required
def checkinOk(request):
    return render(request, 'movil/check-in_ok.html')

@login_required
def busqueda_out(request):
    if request.method == "POST":
        print("Es POST")
        idp = request.POST["idpropiedad"]
        if not idp.isdigit():
            idp = 0
        try:
            idprop = Propiedad.objects.get(id_propiedad=idp)
            idestadores = EstadoReserv.objects.get(id_estado_rese=3)
            res = Reserva.objects.filter(id_propiedad=idprop.id_propiedad, id_estado_rese=idestadores)
            return render(request, 'movil/result_busqueda_out.html', {'res':res})
        except Propiedad.DoesNotExist as den:
            print(den)
            sinres = 0
            return render(request, 'movil/result_busqueda_out.html', {'sinres':sinres})
    else:
        comuna = Comuna.objects.all()
    return render(request, 'movil/busqueda_out.html')

@login_required
def aceptaCheckOut(request, pk):
    res = Reserva.objects.get(id_reserva=pk)
    if request.method == "POST":
        idres = request.POST["idreserva"]
        detalle = request.POST["detalle"]
        montomulta = request.POST["montomulta"]
        obs = request.POST["obs"]

        print("Print Acepta POST id reserva "+idres)
        estadores = EstadoReserv.objects.get(id_estado_rese=5)
        print(estadores)

        rese = Reserva.objects.get(id_reserva=idres)
        rese.id_estado_rese = estadores
        rese.save()

        now = datetime.now()
        #print ("Current date and time : ")
        #print (now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            # create a connection to the Oracle Database
            #connection = cx_Oracle.connect("hr", userpwd, "dbhost.example.com/orclpdb1", encoding="UTF-8")

            cur = conn.cursor()
            cur.callproc('sp_crear_checklist', (now, detalle, obs, montomulta, res.id_reserva))


        except Exception as errr:
            print("error: ", errr)
        else:
            try:
                #cur.callproc('pkg_reservas.sp_crear_reserva', (fechaini, fechafin, cantidad, idpropiedad, idcliente))
                print("Pasó por aquí?")
            except:
                print("No funciono")
            else:
                print("Funciono el procedimiento")
                return redirect('checkoutok')

            finally:
                print("Cerrando Conexión")
                cur.close()
        finally:
            print("Termino el proceso")

        #heckout = CheckList(fecha_check=now, estado_entrega=danno, observaciones=obs, monto_rompepaga=montomulta, id_reserva=res)
        #checkout.save()
    else:
        idprop = Propiedad.objects.get(id_propiedad=res.id_propiedad.id_propiedad)
        prop = DetallePropiedad.objects.filter(id_propiedad=idprop)
        print(prop)
        return render(request, 'movil/check-out.html',{'res':res, 'prop':prop})

@login_required
def checkOutOk(request):
    return render(request, 'movil/check-out_ok.html')

@login_required
def perfil(request):
    user = request.user
    if request.method == "POST":
        nombre = request.POST["nombre"]
        direccion = request.POST["direccion"]
        telefono = request.POST["telefono"]
        comuna = 98
        print(comuna)
        idcom = Comuna.objects.get(id_comuna=comuna)

        cli = Cliente.objects.get(id_cliente=user.id);
        cli.nombres_clien = nombre
        cli.direccion = direccion
        cli.telefono = telefono
        cli.id_comuna = idcom
        cli.save()
        return redirect('perfil')


    else:

        print(user.id)
        prop = Propiedad.objects.all()
        cli = Cliente.objects.get(id_cliente=user.id)
        print(cli.id_cliente)
        res = Reserva.objects.filter(id_cliente=cli)
        comuna = Comuna.objects.all()

        comu = Region()
        com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()

    return render(request, 'core/perfil.html',{'prop': prop, 'cli':cli, 'res':res, 'comuna':comuna, 'com':com})


def team(request):
    prop = Propiedad.objects.all()
    return render(request, 'info/team.html',{'prop': prop})

def roomGrid(request):
    prop = Propiedad.objects.all()
    return render(request, 'propiedades/room-grid.html',{'prop': prop})

@login_required
def preRoomDetail(request, pk):
    detalleprop = Propiedad.objects.get(id_propiedad=pk)

    if request.method == "POST":
        print("Es POST preROOM")

        fechaini = request.POST["fechaini"]
        print(fechaini)
        fechafin = request.POST["fechafin"]
        print(fechafin)
        cantidad = request.POST["huespedes"]
        idprop = Propiedad.objects.get(id_propiedad=pk)
        idpropiedad = idprop.id_propiedad
        print(idpropiedad)
        idcliente = request.POST["idcliente"]
        cliente = Cliente.objects.get(id_cliente=idcliente)
        print("Cliente " + str(cliente.id_cliente))

        try:
            # create a connection to the Oracle Database
            #connection = cx_Oracle.connect("hr", userpwd, "dbhost.example.com/orclpdb1", encoding="UTF-8")

            cur = conn.cursor()
            cur.callproc('pkg_reservas.sp_crear_reserva', (fechaini, fechafin, cantidad, idpropiedad, idcliente))


        except Exception as errr:
            print("error: ", errr)
        else:
            try:
                #cur.callproc('pkg_reservas.sp_crear_reserva', (fechaini, fechafin, cantidad, idpropiedad, idcliente))
                print("Pasó por aquí?")
            except:
                print("No funciono")
            else:
                print("Funciono el procedimiento")

                reserva = Reserva.objects.latest('id_reserva')
                print(reserva.id_reserva)
                mitad_monto = reserva.monto_total / 2

                return render(request, 'pagos/pago_2.html',{'reserva': reserva, 'mitad_monto':mitad_monto})
            finally:
                print("Cerrando Conexión")
                cur.close()
        finally:
            print("Termino el proceso")

        return redirect('home')

    else:
        print("Es GET PRE")
        fechaini = request.GET["fechaini"]
        print(fechaini)
        fechafin = request.GET["fechafin"]
        print(fechafin)
        cantidad = request.GET["huespedes"]
        print(cantidad)

        reserva = Reserva()
        reserva.fecha_inicio_reser = fechaini
        reserva.fecha_termino_reser = fechafin
        reserva.cantidad_acompa = cantidad

        print(reserva.fecha_inicio_reser)

        date_format = "%Y-%m-%d"
        f_ini = datetime.strptime(fechaini, date_format)
        f_fin = datetime.strptime(fechafin, date_format)
        totnoches = f_fin - f_ini

        acomp=int(cantidad) - 1


        prop = Propiedad.objects.get(id_propiedad=pk)
        totestadia = totnoches.days * prop.valor_noche
        print(prop.id_propiedad)
        img = Imagen.objects.filter(id_propiedad=pk)
    return render(request, 'propiedades/preroom-details.html',{'prop': prop, 'img':img, 'reserva':reserva, 'totnoches':totnoches, 'totestadia':totestadia, 'n':range(acomp)})

@login_required
def Pago(request):

    id_reserva = Reserva.objects.latest('id_reserva')
    user = request.user
    if (id_reserva.id_cliente==user.id_cliente):
        print("Son iguales")

    if request.method == "POST":
        print("ES POST EN PAGO")
        montoapagar = request.POST['montoapagar']
        mediopago = request.POST['mediopago']
        id_mpago = FormaPago.objects.get(id_formapag=mediopago)
        idestadopago = EstadoPago.objects.get(idestadopago=1)
        pago = Pago(id_pago=null, abono=montoapagar, monto_pagar=id_reserva.monto_total, id_transaccion=id_reserva.id_reserva, estado="P", id_formapag=id_mpago, id_reserva=id_reserva, idestadopago=idestadopago)
        pago.save()

        return redirect('rexito')
    else:
        print("Es GET EN PAGO")
        prop = Propiedad.objects.all()
    return render(request, 'pagos/pago_2.html',{'prop': prop})

def detallePropiedad(request,pk):

#    useremail = request.user.email
#    clienteaux = ClientePortal.objects.get(email=useremail)
    detalleprop = Propiedad.objects.get(id_propiedad=pk)

    if request.method == "POST":
        fechaini = request.POST["fechaini"]
        print(fechaini)
        fechafin = request.POST["fechafin"]
        print(fechafin)
        cantidad = request.POST["huespedes"]
        idpropiedad = request.POST["idprop"]
        prop = Propiedad.objects.get(id_propiedad=idpropiedad)
        idcliente = request.POST["idcliente"]
        cliente = Cliente.objects.get(id_cliente=idcliente)

        try:
            # create a connection to the Oracle Database
            #connection = cx_Oracle.connect("hr", userpwd, "dbhost.example.com/orclpdb1", encoding="UTF-8")

            cur = conn.cursor()
            cur.callproc('pkg_reservas.sp_crear_reserva', (fechaini, fechafin, cantidad, idpropiedad, idcliente))


        except Exception as errr:
            print("error: ", errr)
        else:
            try:
                #cur.callproc('pkg_reservas.sp_crear_reserva', (fechaini, fechafin, cantidad, idpropiedad, idcliente))
                print("Pasó por aquí?")
            except:
                print("No funciono")
            else:
                print("Funciono el procedimiento")
                return redirect('rexito')
            finally:
                print("Cerrando Conexión")
                cur.close()
        finally:
            print("Termino el proceso")

        return redirect('home')

    else:
        print("Es GET")
        prop = Propiedad.objects.all()
        img = Imagen.objects.filter(id_propiedad=pk)

    return render(request, 'propiedades/room-details.html', {'img': img, 'detalleprop':detalleprop, 'prop':prop })

@login_required
def reservaexito(request):
    prop = Propiedad.objects.all()
    return render(request, 'info/reservaExitosa.html',{'prop': prop})

def Disponibilidad(request):
    if request.method == "POST":
        fechaini = request.POST["fechaini"]
        print(fechaini)
        fechafin = request.POST["fechafin"]
        print(fechafin)
        cantidad = request.POST["huespedes"]

        fini = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
        ffin = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')

        try:
            # create a connection to the Oracle Database
            #connection = cx_Oracle.connect("hr", userpwd, "dbhost.example.com/orclpdb1", encoding="UTF-8")

            cur = conn.cursor()
            cur.callproc('FN_VALIDA_DISPONIBILIDAD', (fini, ffin))


        except Exception as errr:
            print("error: ", errr)
        else:
            try:
                #cur.callproc('pkg_reservas.sp_crear_reserva', (fechaini, fechafin, cantidad, idpropiedad, idcliente))
                print("Pasó por aquí?")
            except:
                print("No funciono")
            else:
                print("Funciono el procedimiento")
                return redirect('rexito')
            finally:
                print("Cerrando Conexión")
                cur.close()
        finally:
            print("Termino el proceso")

        return redirect('home')

    else:
        print("Es GET")
        prop = Propiedad.objects.all()

    return render(request, 'propiedades/room-details.html', {'prop':prop })



def contacto(request):
    prop = Propiedad.objects.all()
    if request.method == 'GET':
        form = ContactForm()
    else:
        request.method == 'POST'
        form = ContactForm()
        subject = request.POST['name']
        from_email = request.POST['email']
        message = request.POST['message']
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
            return redirect('contacto')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('success')
    return render(request, "contacto/contact.html",{'prop': prop})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

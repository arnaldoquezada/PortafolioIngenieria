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
from django.db.models.query import QuerySet
from django_group_by import GroupByMixin
from .models import Imagen, Propiedad, Cliente, Comuna, AuthUser, EstadoCli, Region, Reserva, Propiedades

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


def home(request):

    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()


    if request.method == "POST":
        idc = request.POST["localidades"]
        idcomuna = Comuna.objects.get(id_comuna=idc)

        fechaini = request.POST["arrive"]
        print(fechaini)
        fechafin = request.POST["departure"]
        print(fechafin)
        cantidad = request.POST["huespedes"]

        fini = parse(fechaini)
        print(fini.date())
        ffin = parse(fechafin)
        print(ffin.date())

        reserva = Reserva()
        reserva.num_noche = idcomuna.id_comuna
        reserva.fecha_inicio_reser = fechaini
        reserva.fecha_termino_reser = fechafin
        reserva.cantidad_acompa = cantidad
        print(reserva.num_noche, reserva.fecha_inicio_reser, reserva.fecha_termino_reser, reserva.cantidad_acompa)

        try:

            cursor = conn.cursor()
            return_no = cursor.var(cx_Oracle.CURSOR)
            cursor.callfunc('FN_VALIDA_DISPONIBILIDAD', return_no, [fechaini, fechafin])
            resultado =  return_no.getvalue()
            i = []
            for row in resultado:
                idstring = str(row)
                id_propiedad = int(idstring[1:2])
                idp = Propiedad.objects.get(id_propiedad=id_propiedad)
                i.append(idp)

        except Exception as errr:

            print(type(errr))
            print(errr.args)
            print("error: ", errr)
        else:
            try:
                #cur.callproc('pkg_reservas.sp_crear_reserva', (fechaini, fechafin, cantidad, idpropiedad, idcliente))
                print("Pasó por aquí?")
            except:
                print("No funciono")
            else:
                print("Funciono el procedimiento")
                total = len(i)
                return render(request, 'propiedades/room-list_busqueda.html',{'i': i, 'total':total, 'reserva':reserva, 'com':com })
            finally:
                print("Cerrando Conexión")
                cursor.close()
        finally:
            print("Termino el proceso")

        return redirect('home')
    else:
        prop = Propiedad.objects.all()
        #com = Propiedad.objects.values('id_comuna').annotate(total=Count('id_comuna'))

        return render(request, 'core/home.html',{'prop': prop, 'com':com})

def perfil(request):
    prop = Propiedad.objects.all()
    return render(request, 'core/perfil.html',{'prop': prop})

def team(request):
    prop = Propiedad.objects.all()
    return render(request, 'info/team.html',{'prop': prop})

def roomGrid(request):
    prop = Propiedad.objects.all()
    return render(request, 'propiedades/room-grid.html',{'prop': prop})

def preRoomDetail(request, pk):
    detalleprop = Propiedad.objects.get(id_propiedad=pk)

    if request.method == "POST":
        print("Es POST")
        fechaini = request.POST["fechaini"]
        print(fechaini)
        fechafin = request.POST["fechafin"]
        print(fechafin)
        cantidad = request.POST["huespedes"]
        prop = Propiedad.objects.get(id_propiedad=pk)
        print(prop)
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
        prop = Propiedad.objects.filter(id_propiedad=pk)
        img = Imagen.objects.filter(id_propiedad=pk)
    return render(request, 'propiedades/preroom-details.html',{'prop': prop, 'img':img})

def preRoomDetail0(request, pk):

    if request.method == "POST":
        print("Es POST")
        fechaini = request.POST["fechaini"]
        print(fechaini)
        fechafin = request.POST["fechafin"]
        print(fechafin)
        cantidad = request.POST["huespedes"]
        prop = Propiedad.objects.get(id_propiedad=pk)
        print(prop)

        return render(request, 'propiedades/preroom-details.html',{'detalleprop': detalleprop, 'img':img})

    else:
        print("Es GET")
        prop = Propiedad.objects.filter(id_propiedad=pk)
        print(prop)
        img = Imagen.objects.filter(id_propiedad=pk)
        print(img)
    return render(request, 'propiedades/preroom-details0.html',{'prop': prop, 'img':img})


def Pago(request):
    prop = Propiedad.objects.all()
    return render(request, 'pagos/pago.html',{'prop': prop})

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

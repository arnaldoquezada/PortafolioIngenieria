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
from .models import Imagen, Propiedad, DetallePropiedad, Cliente, Comuna, AuthUser, EstadoCli, Region, Reserva, Propiedades, FormaPago, EstadoPago, Pago, ServicioAdicional, EmpresaExterna, Acompanante
from datetime import date

#conexion base de datos
conn = cx_Oracle.connect("jaybnb","jaybnb","localhost/XE", encoding="UTF-8")

def register(request):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    if request.method == "POST":
        print("Es POST")
        rut = request.POST["run"]
        nombre = request.POST["nombre"]
        apepaterno = request.POST["apepaterno"]
        apematerno = request.POST["apematerno"]
        fechanac = request.POST["fechanac"]
        email = request.POST["email"]
        direccion = request.POST["direccion"]
        comuna = request.POST["comuna"]
        fono = request.POST["telefono"]
        estado = 'S'
        #idcomuna = request.POST.get("comuna")

        idestadocli = EstadoCli.objects.get(id_estado_clie=1)
        print(idestadocli.id_estado_clie)
        #idestado = EstadoCli()
        #idestado.id_estado_clie = idestadocli.id_estado_clie
        idcomuna = Comuna.objects.get(id_comuna=comuna)
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
        comuna = Comuna.objects.all().order_by('nombre_comu')

    return render(request, 'registration/signup.html', {'comuna': comuna, 'com':com})

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

        fini = datetime.strptime(fechaini, '%Y-%m-%d')
        ffin = datetime.strptime(fechafin, '%Y-%m-%d')

        reserva = Reserva()
        reserva.num_noche = idcomuna.id_comuna
        reserva.fecha_inicio_reser = fechaini
        reserva.fecha_termino_reser = fechafin
        reserva.cantidad_acompa = cantidad
        print(reserva.num_noche, reserva.fecha_inicio_reser, reserva.fecha_termino_reser, reserva.cantidad_acompa)

        try:

            cursor = conn.cursor()
            return_no = cursor.var(cx_Oracle.CURSOR)
            if idcomuna.id_comuna == 0:
                cursor.callfunc('pkg_reservas.FN_VALIDA_DISPONIBILIDAD', return_no, [fini, ffin, cantidad])
                resultado =  return_no.getvalue()
                i = []
                for row in resultado:
                    idstring = str(row)
                    id_propiedad = int(idstring[1:2])
                    idp = Propiedad.objects.get(id_propiedad=id_propiedad)
                    i.append(idp)
            else:
                cursor.callfunc('pkg_reservas.FN_DISPONIBILIDAD_POR_COMUNA', return_no, [idcomuna.id_comuna, fini, ffin, cantidad])
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
        prop = Propiedad.objects.all().order_by('-id_propiedad')[:4]
        print(len(prop))
        #com = Propiedad.objects.values('id_comuna').annotate(total=Count('id_comuna'))

        return render(request, 'core/home.html',{'prop': prop, 'com':com})

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

        acomp = Acompanante.objects.all()
        acomplist = []
        for ac in acomp:
            acomplist.append(ac.id_reserva.id_reserva)

        print(acomplist)

    return render(request, 'core/perfil.html',{'prop': prop, 'cli':cli, 'res':res, 'comuna':comuna, 'com':com, 'acomplist':acomplist})

def team(request):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    prop = Propiedad.objects.all()
    return render(request, 'info/team.html',{'prop': prop, 'com':com})

def roomGrid(request):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    prop = Propiedad.objects.all()
    return render(request, 'propiedades/room-grid.html',{'prop': prop, 'com':com})

@login_required
def preRoomDetail(request, pk):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
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
        fini = datetime.strptime(fechaini, '%Y-%m-%d')
        ffin = datetime.strptime(fechafin, '%Y-%m-%d')

        try:
            # create a connection to the Oracle Database
            #connection = cx_Oracle.connect("hr", userpwd, "dbhost.example.com/orclpdb1", encoding="UTF-8")

            cur = conn.cursor()
            cur.callproc('pkg_reservas.sp_crear_reserva', (fini, ffin, cantidad, idpropiedad, idcliente))

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

                #Enviar email al cliente con la info de la reserva
                mensaje = "Se ha generado la reserva N°"+str(reserva.id_reserva)+", los datos han sido enviado a su email."
                subject = "Creación de Reserva - Turismo Real"
                message = "Desde nuestro portal usted ha realizado una reserva de la propiedad "+str(reserva.id_propiedad.nombre_propie)+". Su reserva es la N°"+str(reserva.id_reserva)+". Recuerde que debe cancelar el pago de la reserva antes de 3 horas, de lo contrario su reserva será anulada."
                from_email = cliente.email
                try:
                    send_mail(subject, message, 'contacto@turismo-real.com', [from_email])
                    messages.success(request, mensaje)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

                return redirect('pago')
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
        inv = DetallePropiedad.objects.filter(id_propiedad=pk)
        term = prop.terminos
        terminos = term.split("|")

    return render(request, 'propiedades/preroom-details.html',{'prop': prop, 'inv':inv, 'img':img, 'com':com, 'reserva':reserva, 'totnoches':totnoches, 'totestadia':totestadia, 'n':range(acomp), 'terminos':terminos})

class ServiEx():
    id_serv = 0
    nom_serv = ""
    descrip_serv = ""
    valor_serv = 0
    id_tipo_serv = 0
    foto = ""

@login_required
def Pagos(request):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    id_reserva = Reserva.objects.latest('id_reserva')

    user = request.user
    print(user)
    if (id_reserva.id_cliente.email==user):
        print("Son iguales")

    if request.method == "POST":
        print("ES POST EN PAGO")
        montoapagar = request.POST['montoapagar']
        print(montoapagar)
        mediopago = request.POST['formadepago']
        id_mpago = FormaPago.objects.get(id_formapag=mediopago)
        idestadopago = EstadoPago.objects.get(idestadopago=1)

        try:
            print(id_reserva.id_reserva)
            cur = conn.cursor()
            cur.callproc('pkg_pago.sp_realizar_pago', (int(montoapagar), 999, id_mpago.id_formapag, id_reserva.id_reserva))

            #Bloque Servicio Extras
            serv1 = request.POST.getlist('product')
            servi1canti = request.POST['servi1canti']

            if len(serv1) > 0:
                for precio in serv1:
                    print(precio)
                    separa = precio.split(",")
                    print(separa)
                    idserv1 = separa[1]
                    servi1 = ServicioAdicional.objects.get(id_servicio_extra=idserv1)
                    cur.callproc('PKG_MANEJO_SERV_ADICIONALES.SP_CREAR_RESER_S_EXTRA', (servi1.id_servicio_extra, "", servi1canti, id_reserva.id_reserva))


            #if serv1 != "":
                #cur.callproc('PKG_MANEJO_SERV_ADICIONALES.SP_CREAR_RESER_S_EXTRA', (serv1, "", servi1canti, id_reserva.id_reserva))

            serv2 = request.POST.getlist('producttraslado')
            servi2canti = request.POST['servi2canti']

            if len(serv2) > 0:
                for precio in serv2:
                    print(precio)
                    separa = precio.split(",")
                    print(separa)
                    idserv1 = separa[1]
                    servi2 = ServicioAdicional.objects.get(id_servicio_extra=idserv1)
                    cur.callproc('PKG_MANEJO_SERV_ADICIONALES.SP_CREAR_RESER_S_EXTRA', (servi2.id_servicio_extra, "", servi2canti, id_reserva.id_reserva))
            #if serv2 != "":
                #cur.callproc('PKG_MANEJO_SERV_ADICIONALES.SP_CREAR_RESER_S_EXTRA', (serv2, "", servi2canti, id_reserva.id_reserva))

        except Exception as errr:
            print("error: ", errr)
        else:
            try:
                print("Pasó por aquí?")
            except:
                print("No funciono")
            else:
                print("Funciono el procedimiento")

                reserva = Reserva.objects.latest('id_reserva')
                print(reserva.id_reserva)
                mitad_monto = reserva.monto_total / 2

                if (id_mpago.id_formapag==3):
                    return redirect('transferencia')
                else:
                    return redirect('pagoexito')
            finally:
                print("Cerrando Conexión")
                cur.close()
        finally:
            print("Termino el proceso")

    else:
        print("Es GET EN PAGO")
        prop = Propiedad.objects.all()
        mitad_monto = id_reserva.monto_total / 2
        print(int(mitad_monto))
        emp1 = EmpresaExterna.objects.get(id_empresa_ext=1)
        emp2 = EmpresaExterna.objects.get(id_empresa_ext=2)
        serv1 = ServicioAdicional.objects.filter(id_empresa_ext=emp1.id_empresa_ext);
        print(serv1)
        serv2 = ServicioAdicional.objects.filter(id_empresa_ext=emp2.id_empresa_ext);
        print(serv2)
        print(id_reserva.cantidad_acompa)

        idprop = Propiedad.objects.get(id_propiedad=id_reserva.id_propiedad.id_propiedad)

        obj1 = []
        obj2 = []
        try:

            cursor = conn.cursor()
            return_no = cursor.var(cx_Oracle.CURSOR)
            cursor.callproc('pkg_servicio_adicional.SP_SERVICIOS_ADICIONALES', (idprop.id_propiedad, return_no))
            resultado =  return_no.getvalue().fetchall()

            for row in resultado:
                se = ServiEx()
                if row[5] == 1:
                    se.id_serv = row[0]
                    se.nom_serv = row[1]
                    se.descrip_serv = row[2]
                    se.valor_serv = row[3]
                    se.id_tipo_serv = row[5]
                    se.foto = row[4]
                    obj1.append(se)
                else:
                    se.id_serv = row[0]
                    se.nom_serv = row[1]
                    se.descrip_serv = row[2]
                    se.valor_serv = row[3]
                    se.id_tipo_serv = row[5]
                    se.foto = row[4]
                    obj2.append(se)

            for v in obj1:
                print(v.nom_serv)

            for v in obj2:
                print(v.nom_serv)

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
            finally:
                print("Cerrando Conexión")
                cursor.close()
        finally:
            print("Termino el proceso")

    return render(request, 'pagos/pago.html',{'id_reserva': id_reserva, 'mitad_monto':int(mitad_monto), 'com':com, 'serv1':serv1, 'serv2':serv2, 'obj1':obj1, 'obj2':obj2, 'n':range(1, id_reserva.cantidad_acompa+1) })

@login_required
def PagoReserva(request, pk):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    id_reserva = Reserva.objects.get(id_reserva=pk)
    print(id_reserva)
    user = request.user
    print(user)
    if (id_reserva.id_cliente.email==user):
        print("Son iguales")

    if request.method == "POST":
        print("ES POST EN PAGO")
        montoapagar = request.POST['montoapagar']
        mediopago = request.POST['formadepago']
        id_mpago = FormaPago.objects.get(id_formapag=mediopago)

        try:

            cur = conn.cursor()
            cur.callproc('pkg_pago.sp_realizar_pago_faltante', (int(montoapagar), 999, id_mpago.id_formapag, id_reserva.id_reserva))

        except Exception as errr:
            print("error: ", errr)
        else:
            try:
                print("Pasó por aquí?")
            except:
                print("No funciono")
            else:
                print("Funciono el procedimiento")
                if (id_mpago.id_formapag==3):
                    return redirect('transferencia')
                else:
                    return redirect('pagopendienteexito')
            finally:
                print("Cerrando Conexión")
                cur.close()
        finally:
            print("Termino el proceso")

    else:
        print("Es GET EN PAGO Pendiente")
        pago = Pago.objects.get(id_reserva=id_reserva)

    return render(request, 'pagos/pagoreserva.html',{'id_reserva': id_reserva, 'pago':pago})


@login_required
def pagoexito(request):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    prop = Propiedad.objects.all()
    return render(request, 'info/pagoExitoso.html',{'prop': prop, 'com':com})

@login_required
def pagopendienteexito(request):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    prop = Propiedad.objects.all()
    return render(request, 'info/pagoPendienteExitoso.html',{'prop': prop, 'com':com})

@login_required
def transferencia(request):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    res = Reserva.objects.latest('id_reserva')
    print(res.id_reserva)
    pago = Pago.objects.latest('id_pago')
    print(pago)
    abono = pago.abono - ((pago.abono * 5) /100 )
    abonodesc = int(abono)
    return render(request, 'pagos/pago_transferencia.html',{'res': res, 'abonodesc':abonodesc, 'com':com })

def detallePropiedad(request,pk):

#    useremail = request.user.email
#    clienteaux = ClientePortal.objects.get(email=useremail)
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
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
        inv = DetallePropiedad.objects.filter(id_propiedad=pk)
        term = detalleprop.terminos
        terminos = term.split("|")

    return render(request, 'propiedades/room-details.html', {'img': img, 'inv':inv, 'detalleprop':detalleprop, 'prop':prop, 'com':com, 'terminos':terminos })

@login_required
def reservaexito(request):
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    prop = Propiedad.objects.all()
    return render(request, 'info/reservaExitosa.html',{'prop': prop, 'com':com})

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
    comu = Region()
    com = Propiedades.objects.group_by('id_comuna__id_comuna','id_comuna__nombre_comu').distinct()
    prop = Propiedad.objects.all()

    if request.method == "POST":
        form = ContactForm()
        subject = request.POST['name']
        from_email = request.POST['email']
        message = request.POST['message']
        print(subject+" "+from_email+" "+message)
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ['contacto@turismo-real.com'])
                messages.success(request, 'Su Mensaje fue enviado con éxito, muy pronto se contactarán con usted.')
                return redirect('contacto')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('pagoexito')
        else:
            print("Entro al Else?")
            return HttpResponse('Make sure all fields are entered and valid.')
    else:
        print("Es GET")
        prop = Propiedad.objects.all()
    return render(request, "contacto/contact.html",{'prop': prop, 'com':com})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

#Vista para completar datos de los acompañantes rescata el id reserva
def AgregaAcompanante(request, pk):
    user = request.user
    if request.method == "GET":
        cli = Cliente.objects.get(id_cliente=user.id)
        res = Reserva.objects.get(id_reserva=pk)
        cant = res.cantidad_acompa - 1
    else:
        acomp = ''
        acomp = request.POST.getlist("acomp")

        lista_nueva = []
        for i in range(0, len(acomp), 5):
            lista_nueva.append(acomp[i:i+5])
        print(lista_nueva)

        try:
            # create a connection to the Oracle Database
            #connection = cx_Oracle.connect("hr", userpwd, "dbhost.example.com/orclpdb1", encoding="UTF-8")

            cur = conn.cursor()

            for list in lista_nueva:
                print(list[0], list[1],)
                date_format = "%Y-%m-%d"
                f_nac = datetime.strptime(list[3], date_format)
                cur.callproc('pkg_acompanantes.sp_crear_acompanante', (list[0], list[1],list[2],f_nac,list[4],pk))


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
                return redirect('perfil')
            finally:
                print("Cerrando Conexión")
                cur.close()
        finally:
            print("Termino el proceso")

        return redirect('home')




#        split_strings = [] #El string lo dividimos en grupos de 5 caracateres
#        n = 5
#        for index in range(0, len(acomp), n): #Creamos una lista anidada para dividir los datos de los acompañantes por cada uno
#            split_strings.append(acomp[index : index + n])
#
#        for i in range(len(split_strings)):
#            for j in range(len(split_strings[i])):
#                print("---Print Elements---")
#                print(split_strings[i][j])


        return redirect('perfil')

    return render(request, "propiedades/preroom-datosAcompanante.html",{'cli':cli, 'n':range(cant)})

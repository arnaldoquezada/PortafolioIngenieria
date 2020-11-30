# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models.query import QuerySet
from django_group_by import GroupByMixin


class Acompanante(models.Model):
    id_acompanante = models.IntegerField(primary_key=True)
    nombres = models.TextField()  # This field type is a guess.
    apellido_p = models.TextField()  # This field type is a guess.
    apellido_m = models.TextField()  # This field type is a guess.
    fecha_nac = models.TextField(blank=True, null=True)  # This field type is a guess.
    telefono = models.IntegerField()
    id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva')

    class Meta:
        managed = False
        db_table = 'acompanante'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CheckIn(models.Model):
    idcheck = models.IntegerField(primary_key=True)
    fecha_check = models.TextField()  # This field type is a guess.
    acepta_termino = models.CharField(max_length=1)
    id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva')

    class Meta:
        managed = False
        db_table = 'check_in'


class CheckList(models.Model):
    id_check_list = models.IntegerField(primary_key=True)
    fecha_check = models.TextField()  # This field type is a guess.
    estado_entrega = models.CharField(max_length=1)
    observaciones = models.TextField(blank=True, null=True)  # This field type is a guess.
    monto_rompepaga = models.IntegerField(blank=True, null=True)
    id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva')
    idtiposervex = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'check_list'


class Cliente(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    rut = models.CharField(max_length=13)
    nombres_clien = models.TextField()  # This field type is a guess.
    apellido_p = models.TextField()  # This field type is a guess.
    apellido_m = models.TextField()  # This field type is a guess.
    fecha_nac = models.TextField()  # This field type is a guess.
    email = models.TextField(unique=True)  # This field type is a guess.
    direccion = models.TextField()  # This field type is a guess.
    telefono = models.BigIntegerField(blank=True, null=True)
    estado = models.CharField(max_length=4)
    id_estado_clie = models.ForeignKey('EstadoCli', models.DO_NOTHING, db_column='id_estado_clie')
    id_comuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='id_comuna')
    password = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'cliente'


class Comuna(models.Model):
    id_comuna = models.IntegerField(primary_key=True)
    nombre_comu = models.TextField()  # This field type is a guess.
    id_region = models.ForeignKey('Region', models.DO_NOTHING, db_column='id_region')

    class Meta:
        managed = False
        db_table = 'comuna'


class DetallePropiedad(models.Model):
    id_inventario = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='id_inventario')
    id_propiedad = models.ForeignKey('Propiedad', models.DO_NOTHING, db_column='id_propiedad')
    iddetalle_prop = models.FloatField(primary_key=True)
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_propiedad'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EmpresaExterna(models.Model):
    id_empresa_ext = models.IntegerField(primary_key=True)
    run_empresa = models.TextField(unique=True)  # This field type is a guess.
    nombre_empresa = models.TextField()  # This field type is a guess.
    telefono = models.IntegerField()
    email = models.TextField()  # This field type is a guess.
    estado = models.CharField(max_length=4)
    idtiposerv = models.ForeignKey('TipoServextra', models.DO_NOTHING, db_column='idtiposerv')

    class Meta:
        managed = False
        db_table = 'empresa_externa'


class EstadoCli(models.Model):
    id_estado_clie = models.IntegerField(primary_key=True)
    nombre_estado_cli = models.TextField()  # This field type is a guess.
    descripcion = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'estado_cli'


class EstadoPago(models.Model):
    idestadopago = models.BooleanField(primary_key=True)
    nom_estado_pago = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'estado_pago'


class EstadoPropi(models.Model):
    id_estado_propi = models.IntegerField(primary_key=True)
    nombre_estado = models.TextField()  # This field type is a guess.
    descripcion = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'estado_propi'


class EstadoReserv(models.Model):
    id_estado_rese = models.IntegerField(primary_key=True)
    nombre_reserv = models.TextField()  # This field type is a guess.
    descripcion = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'estado_reserv'


class FormaPago(models.Model):
    id_formapag = models.IntegerField(primary_key=True)
    nombre = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'forma_pago'


class Imagen(models.Model):
    id_imagen = models.IntegerField(primary_key=True)
    ruta_archivo = models.TextField()  # This field type is a guess.
    nombre_archivo = models.TextField()  # This field type is a guess.
    id_propiedad = models.ForeignKey('Propiedad', models.DO_NOTHING, db_column='id_propiedad')

    class Meta:
        managed = False
        db_table = 'imagen'


class Inventario(models.Model):
    id_inventario = models.IntegerField(primary_key=True)
    nombre_inven = models.TextField(unique=True)  # This field type is a guess.
    costo = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=4)
    id_tipo_inven = models.ForeignKey('TipoInventario', models.DO_NOTHING, db_column='id_tipo_inven')

    class Meta:
        managed = False
        db_table = 'inventario'


class Mantencion(models.Model):
    id_mantecion = models.IntegerField(primary_key=True)
    fecha = models.TextField()  # This field type is a guess.
    nombre_contratista = models.TextField()  # This field type is a guess.
    fecha_inicio = models.TextField()  # This field type is a guess.
    fecha_fin = models.TextField()  # This field type is a guess.
    costo = models.IntegerField()
    estado = models.CharField(max_length=4)
    id_propiedad = models.ForeignKey('Propiedad', models.DO_NOTHING, db_column='id_propiedad')
    descrip_mantencion = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mantencion'


class Multa(models.Model):
    id_multa = models.IntegerField(primary_key=True)
    monto_multa = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva')
    fecha_multa = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'multa'


class Pago(models.Model):
    id_pago = models.IntegerField(primary_key=True)
    abono = models.TextField(blank=True, null=True)  # This field type is a guess.
    monto_pagar = models.IntegerField()
    id_transaccion = models.TextField()  # This field type is a guess.
    id_formapag = models.ForeignKey(FormaPago, models.DO_NOTHING, db_column='id_formapag')
    id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva')
    idestadopago = models.ForeignKey(EstadoPago, models.DO_NOTHING, db_column='idestadopago')
    fecha_pago = models.TextField()

    class Meta:
        managed = False
        db_table = 'pago'


class BookQuerySet(QuerySet, GroupByMixin):
    pass

class Propiedades(models.Model):
    objects = BookQuerySet.as_manager()

    id_propiedad = models.IntegerField(primary_key=True)
    rol_propie = models.TextField(unique=True)  # This field type is a guess.
    nombre_propie = models.TextField()  # This field type is a guess.
    avaluo_fiscal = models.IntegerField()
    valor_compra = models.IntegerField()
    direccion = models.TextField()  # This field type is a guess.
    nombre_propietario = models.TextField()  # This field type is a guess.
    run_propietario = models.TextField()  # This field type is a guess.
    pago_contribuciones = models.IntegerField()
    valor_gastosc = models.IntegerField()
    valor_gastosbasic = models.IntegerField()
    nro_habitaciones = models.IntegerField()
    canti_max_ocup = models.IntegerField()
    nro_bathroom = models.IntegerField()
    nro_bodega = models.IntegerField()
    nro_estacionamientos = models.IntegerField()
    nro_cocina = models.IntegerField()
    jardin = models.CharField(max_length=1)
    metros_cuadrados = models.IntegerField()
    inventario_valorizado = models.IntegerField()
    valor_noche = models.IntegerField()
    caracteristicas = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_estado_propi = models.ForeignKey(EstadoPropi, models.DO_NOTHING, db_column='id_estado_propi')
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna')
    imagen_principal = models.TextField()
    terminos = models.TextField()

    class Meta:
        managed = False
        db_table = 'propiedad'


class Propiedad(models.Model):


    id_propiedad = models.IntegerField(primary_key=True)
    rol_propie = models.TextField(unique=True)  # This field type is a guess.
    nombre_propie = models.TextField()  # This field type is a guess.
    avaluo_fiscal = models.IntegerField()
    valor_compra = models.IntegerField()
    direccion = models.TextField()  # This field type is a guess.
    nombre_propietario = models.TextField()  # This field type is a guess.
    run_propietario = models.TextField()  # This field type is a guess.
    pago_contribuciones = models.IntegerField()
    valor_gastosc = models.IntegerField()
    valor_gastosbasic = models.IntegerField()
    nro_habitaciones = models.IntegerField()
    canti_max_ocup = models.IntegerField()
    nro_bathroom = models.IntegerField()
    nro_bodega = models.IntegerField()
    nro_estacionamientos = models.IntegerField()
    nro_cocina = models.IntegerField()
    jardin = models.CharField(max_length=1)
    metros_cuadrados = models.IntegerField()
    inventario_valorizado = models.IntegerField()
    valor_noche = models.IntegerField()
    caracteristicas = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_estado_propi = models.ForeignKey(EstadoPropi, models.DO_NOTHING, db_column='id_estado_propi')
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna')
    imagen_principal = models.TextField()
    terminos = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'propiedad'

class Region(models.Model):
    id_region = models.IntegerField(primary_key=True)
    nombre_reg = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'region'


class RegistroEvento(models.Model):
    id_evento = models.IntegerField(primary_key=True)
    user_evento = models.TextField()  # This field type is a guess.
    descripcion = models.TextField()  # This field type is a guess.
    tipo_evento = models.TextField()  # This field type is a guess.
    evento = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'registro_evento'


class Reserva(models.Model):
    id_reserva = models.IntegerField(primary_key=True)
    fecha_reserva = models.TextField()  # This field type is a guess.
    fecha_inicio_reser = models.TextField()  # This field type is a guess.
    fecha_termino_reser = models.TextField()  # This field type is a guess.
    cantidad_acompa = models.IntegerField()
    num_noche = models.FloatField()
    monto_total = models.IntegerField()
    id_propiedad = models.ForeignKey(Propiedad, models.DO_NOTHING, db_column='id_propiedad')
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_estado_rese = models.ForeignKey(EstadoReserv, models.DO_NOTHING, db_column='id_estado_rese')

    class Meta:
        managed = False
        db_table = 'reserva'


class ReservaSExtra(models.Model):
    id_reserva_s_extra = models.IntegerField(primary_key=True)
    id_reserva = models.ForeignKey(Reserva, models.DO_NOTHING, db_column='id_reserva')
    id_servicio_extra = models.ForeignKey('ServicioAdicional', models.DO_NOTHING, db_column='id_servicio_extra')
    cantidad_servadicional = models.IntegerField()
    total = models.BigIntegerField()
    comentario = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'reserva_s_extra'


class ServicioAdicional(models.Model):
    id_servicio_extra = models.IntegerField(primary_key=True)
    valor_servicio_extra = models.IntegerField()
    estado = models.CharField(max_length=4)
    nombre_servicio = models.TextField()
    descrip_servicio = models.TextField()  # This field type is a guess.
    info_complement = models.TextField()  # This field type is a guess.
    id_empresa_ext = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'servicio_adicional'


class TipoInventario(models.Model):
    id_tipo_inven = models.IntegerField(primary_key=True)
    nombre_tipo = models.TextField()  # This field type is a guess.
    descripcion = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tipo_inventario'


class TipoServextra(models.Model):
    idtiposervex = models.BooleanField(primary_key=True)
    descripcion = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tipo_servextra'


class TipoVehiculo(models.Model):
    idtipove = models.BooleanField(primary_key=True)
    descripcion = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tipo_vehiculo'


class UsuarioSis(models.Model):
    id_user = models.IntegerField(primary_key=True)
    user_name = models.TextField(unique=True)  # This field type is a guess.
    user_pass = models.TextField()  # This field type is a guess.
    nombre_usuario = models.TextField()  # This field type is a guess.
    rol = models.CharField(max_length=1)
    estado = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'usuario_sis'

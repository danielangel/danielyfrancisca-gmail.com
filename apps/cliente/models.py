
from django.db import models
from register.models import User

class Clientesdeudores(models.Model):
    codclideu = models.IntegerField(db_column='CodCliDeu')  # Field name made lowercase.
    rsocial = models.CharField(db_column='Rsocial', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rut = models.CharField(db_column='Rut', max_length=11, blank=True, null=True)
    email = models.CharField(db_column='EMail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    codejec = models.IntegerField(db_column='CodEjec', blank=True, null=True)  # Field name made lowercase.
    cliente = models.BooleanField(db_column='Cliente')  # Field name made lowercase.
    deudor = models.BooleanField(db_column='Deudor')  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    codcomuna = models.IntegerField(db_column='CodComuna', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=30, blank=True, null=True)  # Field name made lowercase.

class Meta:
    managed = False
    db_table = 'ClientesDeudores'

    def __str__(self):
        return selt.rsocial


class Comunas(models.Model):
    codcomuna = models.IntegerField(db_column='CodComuna', blank=True, null=True)  # Field name made lowercase.
    comuna = models.CharField(db_column='Comuna', max_length=50, blank=True, null=True)  # Field name made lowercase.

class Meta:
    managed = False
    db_table = 'Comunas'

    def __str__(self):
        return selt.comuna


class Ejecutivos(models.Model):
    codemp = models.IntegerField(db_column='CodEmp')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellidopaterno = models.CharField(db_column='ApellidoPaterno', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellidomaterno = models.CharField(db_column='ApellidoMaterno', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mailejecutivo = models.CharField(db_column='MailEjecutivo', max_length=150, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nombreusuario = models.CharField(db_column='NombreUsuario', max_length=50, blank=True, null=True)  # Field name made lowercase.

class Meta:
    managed = False
    db_table = 'Ejecutivos'

    def __str__(self):
        return selt.nombre

class Oper(models.Model):
    codcliente = models.IntegerField(db_column='CodCliente', blank=True, null=True)  # Field name made lowercase.
    idoperencurso = models.IntegerField()
    contrato = models.IntegerField(db_column='Contrato', blank=True, null=True)  # Field name made lowercase.
    fechaoper = models.DateTimeField(db_column='FechaOper', blank=True, null=True)  # Field name made lowercase.
    documento = models.CharField(db_column='Documento', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cantdoctos = models.IntegerField(db_column='CantDoctos', blank=True, null=True)  # Field name made lowercase.
    valtotoper = models.DecimalField(db_column='ValTotOper', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    anticipable = models.DecimalField(db_column='Anticipable', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    porcentanticipejec = models.FloatField(db_column='PorcentAnticipEjec', blank=True, null=True)  # Field name made lowercase.
    totalgastos = models.DecimalField(db_column='TotalGastos', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    comisionejec = models.DecimalField(db_column='ComisionEjec', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    iva = models.DecimalField(db_column='IVA', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    aplicaciones = models.IntegerField(db_column='Aplicaciones', blank=True, null=True)  # Field name made lowercase.
    montoagirar = models.DecimalField(db_column='MontoaGirar', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    abonova = models.DecimalField(db_column='AbonoVA', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

class Meta:
    managed = False
    db_table = 'Oper'

    def __str__(self):
        return selt.codcliente


class lineas(models.Model):
    codcliente = models.IntegerField(db_column='codCliente', blank=True, null=True)  # Field name made lowercase.
    linea = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    vigente = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    vctolinea = models.DateField(db_column='vctoLinea', blank=True, null=True)  # Field name made lowercase.

class Meta:
    managed = False
    db_table = 'lineas'

    def __str__(self):
        return selt.codcliente
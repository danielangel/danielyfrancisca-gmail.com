import pyodbc
from django.db import connection
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import *
from apps.cliente.models import *
from register.models import User


# Create your views here.

def index_clientes(request):
    return render(request,'cliente/index.html')

@login_required(login_url='/cliente_listar')
def cliente_list(request):
    if request.user.is_authenticated:
        if (request.user.is_staff == False and request.user.is_active == True):
            query="select c.id	,c.CodCliDeu,c.Rsocial,  c.EMail,(ej.nombre + ej.ApellidoPaterno) as Ejecutivo,c.Direccion, " 
            query=query + " c.CodComuna,c.Telefono from [dbo].[register_user] u INNER JOIN " 
            query=query + " [dbo].[cliente_clientesdeudores] c ON c.Rut=u.rut INNER JOIN  "
            query=query + " [dbo].[cliente_comunas]  CO ON CO.CodComuna=C.CodComuna  "
            query=query + " INNER JOIN [dbo].[cliente_ejecutivos] EJ ON EJ.CodEmp=c.CodEjec"
            query=query + " WHERE c.RUT= '%s'"  %request.user.rut  
            queryset =Clientesdeudores.objects.raw(query )
            contexto = {'object_list':queryset}
            return render(request,'cliente/cliente_list.html', contexto)

@login_required(login_url='/oper_listar')
def cliente_Otorgamiento(request):
    if request.user.is_authenticated:
        if (request.user.is_staff == False and request.user.is_active == True):
            queryset =Clientesdeudores.objects.get(rut=request.user.rut)
            query = "SELECT [id],[CodCliente],[idoperencurso],[Contrato],[FechaOper],[Documento]"        
            query = query + ",[CantDoctos],[ValTotOper],[Anticipable],[PorcentAnticipEjec],[TotalGastos]"   
            query = query + ",[ComisionEjec],[IVA],[Aplicaciones],[MontoaGirar],[AbonoVA] "   
            query = query + " FROM [dbo].[cliente_oper]  WHERE [CodCliente] = %s "  %queryset.codclideu  
            
            queryset =Oper.objects.raw(query )
            contexto = {'object_list':queryset}
            
            return render(request,'cliente/cliente_list_Otorgamiento.html', contexto)




            #with connection.cursor() as cursor:
            #    cursor.execute("{call dbo.spOtorgamientosClienteDeudor(%s)}", [queryset.codclideu])
            #    row =  cursor.fetchall()
            #    contexto = {'object_list':row}
            #    return render(request,'cliente/cliente_list_Otorgamiento.html', contexto)
    
@login_required(login_url='/lineas_listar')
def cliente_lineas(request):
    if request.user.is_authenticated:
        if (request.user.is_staff == False and request.user.is_active == True):
            queryset =Clientesdeudores.objects.get(rut=request.user.rut)
            query = "SELECT	[linea] as Cupo,[vigente] as CupoOcupado,([linea]-[vigente])  as CupoDisponible,[vctoLinea]	"        
            query = query + " [dbo].[Lineas] WHERE [codCliente] = %s "  %queryset.codclideu  
            
            queryset =Oper.objects.raw(query )
            contexto = {'object_list':queryset}
            
            return render(request,'cliente/cliente_list_lineas.html', contexto)

    
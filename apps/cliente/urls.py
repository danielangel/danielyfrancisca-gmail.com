from django.conf.urls import url, include
from apps.cliente.views import  *
# from apps.Clientes.views import  clienteList

app_name = 'cliente'

urlpatterns = [
   # url(r'^$', index_clientes, name='index'),
   # url(r'^nuevo$', cliente_view, name='cliente_crear'),
    url(r'^cliente_listar$', cliente_list, name='cliente_listar'),
    url(r'^oper_listar$', cliente_Otorgamiento , name='oper_listar'),
    url(r'^lineas_listar$', cliente_lineas , name='lineas_listar'),
   # url(r'^listar$', clienteList, name='cliente_listar'),
]
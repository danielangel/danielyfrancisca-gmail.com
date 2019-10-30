from django import forms
from apps.cliente.models import Clientesdeudores

class Clienteform(forms.ModelForm):

    class Meta:
        model = Clientesdeudores

        fields = [
            'rsocial',
            'rut',
            'email',
            'codejec',
            'cliente',
            'deudor',
            'direccion',
            'codcomuna',
            'telefono',
        ]
        labels = {
            'rsocial':  'rsocial',
            'rut': 'rut',
            'email': 'email',
            'codejec': 'codejec',
            'cliente': 'cliente'
          #  'deudor': 'deudor',
           # 'direccion': 'direccion',
           # 'codcomuna': 'codcomuna',
           # 'telefono': 'telefono'
        }
        widgets = {
            'rsocial':  forms.TextInput(attrs={'class':'form-control'}),
            'rut': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            #'codejec': forms.TextInput(attrs={'class':'form-control'}),
            #'cliente': forms.TextInput(attrs={'class':'form-control'}),
            #'deudor': forms.TextInput(attrs={'class':'form-control'}),
            #'direccion': forms.TextInput(attrs={'class':'form-control'}),
            #'codcomuna': forms.TextInput(attrs={'class':'form-control'}),
            #'telefono': forms.TextInput(attrs={'class':'form-control'}),
        }
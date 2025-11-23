from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "sku",
            "nombre",
            "descripcion",
            "categoria",
            "precio",
            "stock",
            "stock_minimo",
            "imagen",
        ]

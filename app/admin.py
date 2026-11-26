from django.contrib import admin
from .models import Servico, Categoria, Contato, Pedido, ItemPedido

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Servico)
admin.site.register(Contato)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
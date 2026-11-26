from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quem-somos/", views.quem_somos, name="quem_somos"),
    path("servicos", views.servicos, name="servicos"),
    path("produtos", views.produtos, name="produtos"),
    path("add-servicos", views.addServicos, name="addServicos"),
    path("del-servicos/<int:id_servico>", views.delServicos, name="delServicos"),
    path("edit-servicos/<int:id_servico>", views.editServicos, name="editServicos"),
    path("contato/add-contato/", views.add_contato, name="add_contato"),
    path("contato/contatos/", views.contatos, name="contatos"),
    path("contato/del-contato/<int:id_contato>/", views.del_contato, name="del_contato"),
    path("integrantes", views.integrantes, name="integrantes"),
    path("add-integrante", views.addIntegrante, name="addIntegrante"),
    path("edit-integrante/<int:id_integrante>", views.editIntegrante, name="editIntegrante"),
    path("del-integrante/<int:id_integrante>", views.delIntegrante, name="delIntegrante"),

    # Carrinho e Pedidos
    path("carrinho/", views.carrinho, name="carrinho"),
    path("produtos/adicionar/<int:id_servico>/", views.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path("carrinho/remover/<int:id_item>/", views.remover_do_carrinho, name="remover_do_carrinho"),
    path("carrinho/editar/<int:id_item>/", views.editar_item_carrinho, name="editar_item_carrinho"),
    path("carrinho/finalizar/", views.finalizar_pedido, name="finalizar_pedido"),
    path("meus-pedidos/", views.meus_pedidos, name="meus_pedidos"),

    path('categoria-api/', views.categoriasAPI, name='categoriasAPI'),
    path('categoria-api/<int:id_categoria>', views.categoriaAPI, name='categoriaAPI'
    ),
    path('relatorios/', views.relatorios, name='relatorios')
]

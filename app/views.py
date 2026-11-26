import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import FormContato, FormServico
from .models import Categoria, Contato, Pedido, ItemPedido, Servico
from .serializers import CategoriaSerializer
from .supabase_client import supabase


def quem_somos(request):
    """Página Quem Somos - com equipe do Supabase"""
    resposta = supabase.table("integrantes").select("*").execute()
    integrantes = resposta.data if resposta.data else []
    
    return render(request, "quem-somos.html", {"integrantes": integrantes})


@login_required
def carrinho(request):
    """Mostra o carrinho do usuário logado"""
    pedido, criado = Pedido.objects.get_or_create(
        usuario=request.user,
        ativo=True,
        defaults={'total': 0}
    )

    itens = pedido.itens.all()
    total = sum(item.subtotal() for item in itens) if itens else 0

    return render(request, "carrinho.html", {
        'pedido': pedido,
        'itens': itens,
        'total': total,
    })


@login_required
def adicionar_ao_carrinho(request, id_servico):
    """Adiciona um serviço ao carrinho"""
    servico = get_object_or_404(Servico, id=id_servico)

    # Busca ou cria o carrinho ativo do usuário
    pedido, criado = Pedido.objects.get_or_create(
        usuario=request.user,
        ativo=True,
        defaults={'total': 0}
    )

    # Busca se o item já existe no carrinho
    item, item_criado = ItemPedido.objects.get_or_create(
        pedido=pedido,
        servico=servico,
        defaults={'quantidade': 1, 'preco': servico.preco}
    )

    if not item_criado:
        item.quantidade += 1
        item.save()

    return redirect('carrinho')


@login_required
def remover_do_carrinho(request, id_item):
    """Remove um item do carrinho"""
    item = get_object_or_404(ItemPedido, id=id_item)
    item.delete()
    return redirect('carrinho')


@login_required
def finalizar_pedido(request):
    """Finaliza o pedido atual"""
    pedido = Pedido.objects.filter(usuario=request.user, ativo=True).first()

    if pedido and pedido.itens.exists():
        pedido.ativo = False
        pedido.calcular_total()
        pedido.save()

        # Criar novo carrinho para o usuário
        Pedido.objects.create(usuario=request.user, total=0)

    return redirect('meus_pedidos')


@login_required
def meus_pedidos(request):
    """Mostra os pedidos do usuário"""
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_pedido')

    return render(request, "meus-pedidos.html", {
        'pedidos': pedidos,
    })


@staff_member_required
def integrantes(request):
    resposta = supabase.table("integrantes").select("*").execute()

    return render(request, "integrantes.html", {"integrantes": resposta.data})


# Create your views here.
def index(request):
    return render(request, "index.html")


def servicos(request):

    # servicos = Servico.objects.all()
    # filter() filtra a busca
    servicos = Servico.objects.filter(ativo=True)
    servicos = servicos.exclude(preco=0)

    # count() total de objetos
    total_servicos = servicos.count()
    # exists() verifica se existem objetos
    tem_servicos = servicos.exists()
    # order_by(): ordena os objetos

    mais_barato = servicos.order_by("preco").first()
    mais_caro = servicos.order_by("-preco").first()

    # recupera o valor do form
    busca = request.GET.get("busca")

    if busca:
        servicos = servicos.filter(nome__icontains=busca)

    categorias = Categoria.objects.filter(ativo=True)

    categoria = request.GET.get("categoria")

    if categoria:
        servicos = servicos.filter(categoria_id=categoria)

    preco = request.GET.get("preco")

    if preco == "baixo":
        servicos = servicos.filter(preco__lte=500)
    elif preco == "medio":
        servicos = servicos.filter(preco__gte=500, preco__lte=1500)
    elif preco == "alto":
        servicos = servicos.filter(preco__gt=1500)

    ordem = request.GET.get("ordem")

    if ordem == "menor":
        servicos = servicos.order_by("preco")  # ordena crescente
    elif ordem == "maior":
        servicos = servicos.order_by("-preco")  # ordena por preco descrescente
    elif ordem == "nome":
        servicos = servicos.order_by("nome")  # ordena por nome A-Z
    else:
        servicos = servicos.order_by("nome")

    contexto = {
        "servicos": servicos,
        "is_admin": request.user.is_staff or request.user.is_superuser,
        "total_servicos": total_servicos,
        "tem_servicos": tem_servicos,
        "mais_barato": mais_barato,
        "mais_caro": mais_caro,
        "categorias": categorias,
        "categoria": categoria,
        "preco": preco,
        "ordem": ordem,
    }

    return render(request, "servicos.html", contexto)


def produtos(req):
    produtos = Servico.objects.filter(ativo=True)

    res = requests.get("https://fakestoreapi.com/products")
    produtos_api = res.json()

    return render(
        req, "produtos.html", {"servicos": produtos, "produtos_api": produtos_api}
    )


@staff_member_required
def addServicos(request):
    form = FormServico(request.POST, request.FILES or None)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("servicos")

    return render(request, "add-servicos.html", {"form": form})


@staff_member_required
def delServicos(request, id_servico):
    servico = Servico.objects.get(id=id_servico)
    servico.delete()
    return redirect("servicos")


@staff_member_required
def editServicos(request, id_servico):
    servico = Servico.objects.get(id=id_servico)
    form = FormServico(request.POST or None, instance=servico)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("servicos")

    return render(request, "edit-servicos.html", {"form": form})


def add_contato(request):
    form = FormContato(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("contatos")
    return render(request, "add-contato.html", {"form": form})


@staff_member_required
def contatos(request):
    return render(request, "contatos.html", {"contatos": Contato.objects.all()})


@staff_member_required
def del_contato(request, id_contato):
    contato = get_object_or_404(Contato, id=id_contato)
    contato.delete()
    return redirect("contatos")


@staff_member_required
def addIntegrante(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cargo = request.POST.get("cargo")
        biografia = request.POST.get("biografia")
        foto_url = request.POST.get("foto") or None

        response = (
            supabase.table("integrantes")
            .insert(
                {
                    "nome": nome,
                    "cargo": cargo,
                    "biografia": biografia,
                    "foto_url": foto_url,
                }
            )
            .execute()
        )

        return redirect("integrantes")

    return render(request, "add-integrante.html")


@staff_member_required
def delIntegrante(request, id_integrante):
    supabase.table("integrantes").delete().eq("id", id_integrante).execute()
    return redirect("integrantes")


@staff_member_required
def editIntegrante(request, id_integrante):
    """Edita um integrante existente no Supabase"""
    # Busca o integrante atual
    response = supabase.table("integrantes").select("*").eq("id", id_integrante).execute()
    integrante = response.data[0] if response.data else None

    if not integrante:
        return redirect("integrantes")

    if request.method == "POST":
        nome = request.POST.get("nome")
        cargo = request.POST.get("cargo")
        biografia = request.POST.get("biografia")
        foto_url = request.POST.get("foto") or integrante.get("foto_url")

        supabase.table("integrantes").update({
            "nome": nome,
            "cargo": cargo,
            "biografia": biografia,
            "foto_url": foto_url,
        }).eq("id", id_integrante).execute()

        return redirect("integrantes")

    return render(request, "edit-integrante.html", {"integrante": integrante})


@api_view(["GET"])
def categoriasAPI(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)


@api_view(["GET", "DELETE"])
def categoriaAPI(request, id_categoria):
    categoria = Categoria.objects.get(id=id_categoria)
    if request.method == "GET":
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    elif request.method == "DELETE":
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@staff_member_required
def relatorios(request):

    servicos = Servico.objects.all()

    servicos_ativos = servicos.filter(ativo=True).count()

    servicos_inativos = servicos.filter(ativo=False).count()

    categorias = servicos.values("categoria__nome").annotate(quantidade=Count("id"))

    return render(
        request,
        "relatorio.html",
        {
            "servicos_ativos": servicos_ativos,
            "servicos_inativos": servicos_inativos,
            "categorias_labels": [
                item["categoria__nome"] or "Sem categoria" for item in categorias
            ],
            "categorias_valores": [item["quantidade"] for item in categorias],
        },
    )


@login_required
def editar_item_carrinho(request, id_item):
    """Edita a quantidade de um item no carrinho"""
    item = get_object_or_404(ItemPedido, id=id_item, pedido__usuario=request.user)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))
        if quantidade > 0:
            item.quantidade = quantidade
            item.save()
        else:
            item.delete()
        return redirect('carrinho')

    return render(request, "editar-item-carrinho.html", {'item': item})

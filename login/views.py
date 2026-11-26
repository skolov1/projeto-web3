from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Count
from .forms import CadastroForm
from app.models import Pedido, Servico, Categoria


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.is_staff or user.is_superuser:
                return redirect('/admin/')

            return redirect('dashboard')

    from django.contrib.auth.views import LoginView
    return LoginView.as_view(template_name='login.html')(request)


@login_required
def dashboard(request):
    user = request.user
    is_admin = user.is_staff or user.is_superuser

    # Dados para gráficos
    if is_admin:
        # Admin vê dados globais
        pedidos = Pedido.objects.all()
        servicos = Servico.objects.all()
    else:
        # Cliente vê apenas seus dados
        pedidos = Pedido.objects.filter(usuario=user)
        servicos = Servico.objects.none()  # Cliente não vê stats de serviços

    # Stats de pedidos
    total_pedidos = pedidos.count()
    pedidos_ativos = pedidos.filter(ativo=True).count()
    pedidos_finalizados = pedidos.filter(ativo=False).count()

    # Valor total gasto (apenas finalizados)
    from django.db.models import Sum
    total_gasto = pedidos.filter(ativo=False).aggregate(
        total=Sum('total')
    )['total'] or 0

    # Pedidos por mês (últimos 6 meses)
    from django.utils import timezone
    from datetime import timedelta
    import json

    if is_admin:
        seis_meses_atras = timezone.now() - timedelta(days=180)
        pedidos_mes = pedidos.filter(data_pedido__gte=seis_meses_atras).extra(
            select={'mes': "strftime('%%Y-%%m', data_pedido)"}
        ).values('mes').annotate(count=Count('id')).order_by('mes')

        meses_labels = [item['mes'] for item in pedidos_mes]
        meses_valores = [item['count'] for item in pedidos_mes]

        servicos_ativos = servicos.filter(ativo=True).count()
        servicos_inativos = servicos.filter(ativo=False).count()
        categorias_qs = servicos.values("categoria__nome").annotate(quantidade=Count("id"))
        categorias_labels = [item["categoria__nome"] or "Sem categoria" for item in categorias_qs]
        categorias_valores = [item["quantidade"] for item in categorias_qs]
    else:
        meses_labels = meses_valores = []
        servicos_ativos = servicos_inativos = 0
        categorias_labels = categorias_valores = []

    context = {
        'total_pedidos': total_pedidos,
        'pedidos_ativos': pedidos_ativos,
        'pedidos_finalizados': pedidos_finalizados,
        'total_gasto': total_gasto,
        'meses_labels': json.dumps(meses_labels),
        'meses_valores': json.dumps(meses_valores),
        'servicos_ativos': servicos_ativos,
        'servicos_inativos': servicos_inativos,
        'categorias_labels': json.dumps(categorias_labels),
        'categorias_valores': json.dumps(categorias_valores),
        'is_admin': is_admin,
    }

    return render(request, "dashboard.html", context)

@login_required
def perfil(request):

    if request.method == "POST":
        usuario = request.user

        usuario.first_name = request.POST.get("nome")
        usuario.last_name = request.POST.get("sobrenome")
        usuario.email = request.POST.get("email")

        usuario.save()

        return redirect("dashboard")



    return render(request, "perfil.html")

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = CadastroForm()


    return render(request, 'cadastro.html', {'form': form})

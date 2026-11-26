## WEB III – Projeto Django

Desenvolver uma página inicial (Home) que apresente informações gerais sobre o

sistema, utilizando um tema visual de livre escolha e disponibilizando um menu de

navegação com as seguintes opções: Quem Somos, Produtos, Contato e Entrar.

A página “Quem Somos” deve apresentar informações institucionais sobre a empresa e os integrantes da equipe. Os dados dos integrantes deverão ser consultados em um

banco de dados remoto utilizando o Supabase.


A página “Produtos” deverá apresentar os produtos cadastrados no banco de dados

local e os produtos obtidos por meio de uma API externa. Os produtos cadastrados localmente deverão possuir um botão “Comprar”, permitindo que clientes autenticados

adicionem esses produtos aos seus pedidos. A funcionalidade de compra deverá estar

disponível exclusivamente para usuários logados no sistema.

A página “Contatos” deverá conter um formulário que permita aos visitantes entrar em contato com a empresa, enviando dúvidas, sugestões ou solicitações, sem a

necessidade de autenticação ou realização de login.


Ao clicar na opção “Entrar”, o usuário deverá visualizar as opções para realizar o login,

recuperar a senha caso tenha esquecido ou, se ainda não possuir uma conta, efetuar seu cadastro no sistema (Novo Usuário).

## Novo Usuário:


A página “Esqueceu a Senha” deverá utilizar o mecanismo nativo de recuperação de

senhas do Django, permitindo que o usuário solicite a redefinição de sua senha de forma segura.

Caso o usuário realize o login com perfil de administrador (Admin), deverá ser

redirecionado automaticamente para o painel administrativo do Django.


## Painel Administrativo do Django:

Caso o usuário realize o login com perfil de cliente, deverá ser redirecionado automaticamente para a Dashboard.


A página “Dashboard” deverá exibir, no menu principal, as opções “Dashboard” e

“Sair”. No conteúdo da página, deverá apresentar o nome do usuário logado e as seções disponíveis para acesso, conforme suas permissões: Editar Perfil, Contatos,

Serviços, Equipe, Meus Pedidos e Relatórios.

A página “Editar Perfil” deverá apresentar as informações cadastrais do usuário

logado, permitindo a visualização e a edição de seus dados, além de disponibilizar um link para alteração de senha.


## Alterar Senha:

A página “Contatos” deverá exibir as mensagens recebidas por meio do formulário de contato da empresa, permitindo ao usuário visualizar o conteúdo das mensagens e

realizar a exclusão dos registros quando necessário.


A página “Serviços” deverá apresentar todos os serviços cadastrados no sistema,

disponibilizando filtros para personalizar a listagem e dados estatísticos sobre os serviços. Também deverá oferecer as opções de adicionar novo serviço, editar e

excluir os registros existentes.

## Novo Serviço:


## Editar Serviço:

A página “Equipe” deverá apresentar todos os integrantes cadastrados no banco de dados remoto (Supabase), disponibilizando as opções de adicionar novos integrantes,

editar informações e excluir os registros existentes.


## Novo Integrante:

## Editar Integrante:


A página “Meus Pedidos” deverá apresentar todos os produtos selecionados e

adicionados ao carrinho pelo usuário na página “Produtos”, permitindo a visualização dos itens adquiridos e das informações relacionadas aos pedidos realizados.

A página “Relatórios” deverá apresentar gráficos e dados estatísticos referentes aos

serviços cadastrados no sistema, permitindo visualizar e analisar informações relevantes por meio de representações gráficas e indicadores quantitativos.

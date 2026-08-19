import os

from pydantic import BaseModel

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_session import Session

from backend.database.models.site_schemas import UniversidadeModel
from backend.database.models.return_schemas import UserVerification, StatusResponse

from backend.utils.user_utils import validar_criar__user, desativar_user_by_id, atualizar_user
from backend.utils.universidade_utils import deletar_universidade_by_id, criar_universidade, atualizar_dados_universidade

from backend.services.site_services import get_dashboard_admin_data, get_admin_users, get_admin_projetos, get_admin_candidaturas, get_admin_propostas, get_universidades, get_admin_user_data, get_universidades_detalhado

app = Flask(__name__, template_folder="./frontend/templates")

app.static_folder = './frontend/src'
app.static_url_path = '/static'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret")
app.config['SESSION_TYPE'] = 'filesystem'

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False
)

Session(app)

"""
GERAL
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # autenticação aqui

        return redirect("/dashboard")

    return render_template("login.html")

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nome = request.form.get("name")
        sobrenome = request.form.get("lastname")
        email = request.form.get("email")
        universidade = request.form.get("university")
        senha = request.form.get("password")
        senha_confirmacao = request.form.get("password_confirm")

        # criação do usuário aqui

        return redirect("/login")

    return render_template("registro.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard_aluno.html")

@app.route("/logout")
def logout():
    pass

@app.route("/forgot-password")
def forgot_password():
    pass

"""
PAGINAS ADMIN
"""
@app.route("/admin")
def admin_dashboard():
    dashboard_data: BaseModel = get_dashboard_admin_data()
    
    return render_template("dashboard_admin.html", **dashboard_data.model_dump())
    
@app.route("/admin/usuarios")
def admin_usuarios():
    usuarios: list = get_admin_users()
    dashboard_data: BaseModel = get_dashboard_admin_data()

    return render_template("admin/usuarios.html", usuarios=usuarios, **dashboard_data.model_dump())
    
@app.route("/admin/usuarios/novo", methods=["GET", "POST"])
def admin_novo_usuario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        telegram_id = request.form.get("telegram_id", "").strip() or None
        senha = request.form.get("senha", "")
        role = request.form.get("role", "user")
        tipo = request.form.get("tipo")

        universidade_id = request.form.get("universidade_id")
        ativo = request.form.get("ativo") == "on"

        matricula = request.form.get("matricula", "").strip()
        curso = request.form.get("curso", "").strip()
        periodo = request.form.get("periodo")
        lattes = request.form.get("lattes", "").strip() or None
        previsao_conclusao = request.form.get("previsao_conclusao", "").strip() 

        departamento = request.form.get("departamento", "").strip()
        area_pesquisa = request.form.get("area_pesquisa", "").strip()
        sala = request.form.get("sala", "").strip() or None

        data_user: BaseModel = UserVerification(
            nome=nome,
            username=username,
            email=email,
            telegram_id=telegram_id,
            senha=senha,
            role=role,
            tipo=tipo,
            universidade_id=universidade_id,
            ativo=ativo,
            matricula=matricula,
            curso=curso,
            periodo=periodo,
            lattes=lattes,
            previsao_conclusao=previsao_conclusao,
            departamento=departamento,
            area_pesquisa=area_pesquisa,
            sala=sala
        )
        
        valido: StatusResponse = validar_criar__user(data_user)
        if valido.success:
            flash(valido.status, "success")
            return redirect(url_for("admin_usuarios"))
        else:
            flash(valido.status, "danger")
    
    universidades = get_universidades()

    return render_template("admin/novo_usuario.html", universidades=universidades)

@app.route("/admin/usuarios/<int:usuario_id>/excluir", methods=["POST"])
def admin_excluir_usuario(usuario_id):
    resposta = desativar_user_by_id(usuario_id)

    flash(resposta.status, "success" if resposta.success else "danger")

    return redirect(url_for("admin_usuarios"))

@app.route("/admin/usuarios/<int:usuario_id>/editar", methods=["GET", "POST"])
def admin_editar_usuario(usuario_id):
    if request.method == 'POST':
        nome = request.form.get("nome", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        telegram_id = request.form.get("telegram_id", "").strip()
        senha = request.form.get("senha", "")
        role = request.form.get("role", "user")
        tipo = request.form.get("tipo")

        universidade_id = request.form.get("universidade_id")
        ativo = request.form.get("ativo") == "on"

        matricula = request.form.get("matricula", "").strip()
        curso = request.form.get("curso", "").strip()
        periodo = request.form.get("periodo")
        lattes = request.form.get("lattes", "").strip()
        previsao_conclusao = request.form.get("previsao_conclusao", "").strip()

        departamento = request.form.get("departamento", "").strip()
        area_pesquisa = request.form.get("area_pesquisa", "").strip()
        sala = request.form.get("sala", "").strip()

        data_user: BaseModel = UserVerification(
            id=usuario_id,
            nome=nome,
            username=username,
            email=email,
            telegram_id=telegram_id,
            senha=senha,
            role=role,
            tipo=tipo,
            universidade_id=universidade_id,
            ativo=ativo,
            matricula=matricula,
            curso=curso,
            periodo=periodo,
            lattes=lattes,
            previsao_conclusao=previsao_conclusao,
            departamento=departamento,
            area_pesquisa=area_pesquisa,
            sala=sala
        )
        
        user_atualizado = atualizar_user(data_user)
        
        if not user_atualizado:
            flash("User não encontrado", "danger")
        else:
            flash("User atualizado com sucesso", "success")
    
    universidades = get_universidades()
    data: BaseModel = get_admin_user_data(usuario_id)

    return render_template("admin/editar_usuario.html", universidades=universidades, **data.model_dump())

@app.route("/admin/usuarios/<int:usuario_id>/visualizar")
def admin_visualizar_usuario(usuario_id):
    data_user: BaseModel = get_admin_user_data(usuario_id)
    projetos = get_admin_projetos(user_id=usuario_id)

    return render_template("admin/visualizar_usuario.html", projetos=projetos, **data_user.model_dump())

@app.route("/admin/projetos")
def admin_projetos():
    projetos = get_admin_projetos()
    dashboard_data: BaseModel = get_dashboard_admin_data()
    
    return render_template("admin/projetos.html", projetos=projetos, **dashboard_data.model_dump())

@app.route("/admin/candidaturas")
def admin_candidaturas():
    candidaturas: list = get_admin_candidaturas()
    dashboard_data: BaseModel = get_dashboard_admin_data()

    return render_template("admin/candidaturas.html", candidaturas=candidaturas, **dashboard_data.model_dump())

@app.route("/admin/propostas")
def admin_propostas():
    propostas = get_admin_propostas()
    dashboard_data: BaseModel = get_dashboard_admin_data()

    return render_template("admin/propostas.html", propostas=propostas, **dashboard_data.model_dump())

@app.route("/admin/universidades")
def admin_universidades():
    universidades = get_universidades_detalhado()
    estados = [u.estado for u in universidades]
    dashboard_data: BaseModel = get_dashboard_admin_data()
    
    return render_template("admin/universidades.html", universidades=universidades, estados=estados, **dashboard_data.model_dump())

@app.route("/admin/universidades/novo", methods=["POST"])
def admin_nova_universidade():
    try:
        universidade = UniversidadeModel(
            nome=request.form.get("nome", "").strip(),
            sigla=request.form.get("sigla", "").strip().upper(),
            cidade=request.form.get("cidade", "").strip(),
            estado=request.form.get("estado", "").strip().upper()
        )

        criar_universidade(universidade)

        flash("Universidade criada com sucesso.", "success")

    except Exception as e:
        flash(f"Erro ao criar universidade: {str(e)}", "danger")

    return redirect(url_for("admin_universidades"))

@app.route("/admin/universidades/<int:universidade_id>/editar", methods=["POST"])
def admin_atualizar_universidade(universidade_id):
    try:
        universidade = UniversidadeModel(
            id=universidade_id,
            nome=request.form.get("nome", "").strip(),
            sigla=request.form.get("sigla", "").strip().upper(),
            cidade=request.form.get("cidade", "").strip(),
            estado=request.form.get("estado", "").strip().upper()
        )

        universidade_atualizada = atualizar_dados_universidade(universidade)

        if not universidade_atualizada:
            flash("Universidade não encontrada.", "danger")
        else:
            flash("Universidade atualizada com sucesso.", "success")

    except Exception as e:
        flash(f"Erro ao atualizar universidade: {str(e)}", "danger")

    return redirect(url_for("admin_universidades"))

@app.route("/admin/universidades/<int:universidade_id>/excluir", methods=["POST"])
def admin_excluir_universidade(universidade_id):
    resposta = deletar_universidade_by_id(universidade_id)

    flash(resposta.status, "success" if resposta.success else "danger")

    return redirect(url_for("admin_universidades"))

@app.route("/admin/configuracoes")
def admin_configuracoes():
    configuracoes = {
        "nome_plataforma": "Orienta.IA",

        "descricao": (
            "Plataforma para conectar estudantes, "
            "professores e oportunidades acadêmicas."
        ),

        "email_administrativo": "admin@orientaia.com.br",

        # Usuários
        "permitir_cadastro": True,
        "aprovar_cadastro": False,
        "permitir_telegram": True,

        # Projetos
        "permitir_projetos": True,
        "permitir_candidaturas": True,
        "permitir_propostas": True,

        # Notificações
        "notificacoes_email": True,
        "notificacoes_sistema": True,

        # Segurança
        "tempo_sessao": 60,
        "tentativas_login": 5,

        # Manutenção
        "modo_manutencao": False,
    }

    return render_template("admin/configuracoes.html", configuracoes=configuracoes)
    
@app.route("/admin/dados")
def admin_dados():

    dados = {
        "total_registros": 287,
        "usuarios": 42,
        "estudantes": 28,
        "professores": 8,
        "universidades": 3,
        "projetos": 31,
        "cronogramas": 96,
        "solicitacoes_projeto": 18,
        "solicitacoes_cancelamento": 4,
        "solicitacoes_vincular": 7,

        "ultima_verificacao": "12/08/2026 às 13:32",
        "status_banco": "online",
    }

    modelos = [
        {
            "nome": "Usuários",
            "tabela": "users",
            "descricao": "Contas e informações básicas dos usuários.",
            "registros": 42,
            "icone": "bi-people",
            "url": "admin_usuarios",
        },
        {
            "nome": "Estudantes",
            "tabela": "estudante",
            "descricao": "Dados acadêmicos dos estudantes.",
            "registros": 28,
            "icone": "bi-mortarboard",
            "url": None,
        },
        {
            "nome": "Professores",
            "tabela": "professor",
            "descricao": "Dados acadêmicos e profissionais dos professores.",
            "registros": 8,
            "icone": "bi-person-workspace",
            "url": None,
        },
        {
            "nome": "Universidades",
            "tabela": "universidade",
            "descricao": "Instituições cadastradas na plataforma.",
            "registros": 3,
            "icone": "bi-building",
            "url": "admin_universidades",
        },
        {
            "nome": "Projetos",
            "tabela": "projetos",
            "descricao": "Projetos de iniciação científica, TCC e orientação.",
            "registros": 31,
            "icone": "bi-folder",
            "url": "admin_projetos",
        },
        {
            "nome": "Cronogramas",
            "tabela": "cronograma",
            "descricao": "Etapas e cronogramas dos projetos.",
            "registros": 96,
            "icone": "bi-calendar3",
            "url": None,
        },
        {
            "nome": "Solicitações de projeto",
            "tabela": "solicitacao_projeto",
            "descricao": "Solicitações de estudantes para projetos.",
            "registros": 18,
            "icone": "bi-file-earmark-plus",
            "url": "admin_propostas",
        },
        {
            "nome": "Cancelamentos",
            "tabela": "projeto_cancelamento",
            "descricao": "Solicitações de cancelamento de projetos.",
            "registros": 4,
            "icone": "bi-x-circle",
            "url": None,
        },
        {
            "nome": "Vinculações",
            "tabela": "solicitacoes_vincular",
            "descricao": "Solicitações de vínculo com universidades.",
            "registros": 7,
            "icone": "bi-link-45deg",
            "url": None,
        },
    ]

    return render_template("admin/dados.html", dados=dados, modelos=modelos)

@app.route("/admin/notificoes")
def admin_notificacoes():

    notificacoes = [
        {
            "id": 1,
            "titulo": "Nova proposta de projeto",
            "mensagem": (
                "Uma nova proposta foi enviada para o projeto "
                "de Inteligência Artificial."
            ),
            "tipo": "projeto",
            "destinatario": "Professores",
            "destinatarios": 8,
            "data": "12/08/2026 13:21",
            "lida": False,
            "status": "enviada",
            "icone": "bi-folder-plus"
        },
        {
            "id": 2,
            "titulo": "Novo usuário cadastrado",
            "mensagem": (
                "Um novo estudante acabou de criar uma conta "
                "no Orienta.IA."
            ),
            "tipo": "usuario",
            "destinatario": "Administradores",
            "destinatarios": 2,
            "data": "12/08/2026 12:48",
            "lida": True,
            "status": "enviada",
            "icone": "bi-person-plus"
        },
        {
            "id": 3,
            "titulo": "Solicitação de cancelamento",
            "mensagem": (
                "Foi solicitada a interrupção de um projeto "
                "de iniciação científica."
            ),
            "tipo": "solicitacao",
            "destinatario": "Professores",
            "destinatarios": 8,
            "data": "12/08/2026 11:32",
            "lida": False,
            "status": "enviada",
            "icone": "bi-exclamation-circle"
        },
        {
            "id": 4,
            "titulo": "Manutenção programada",
            "mensagem": (
                "O sistema passará por manutenção programada "
                "nesta noite."
            ),
            "tipo": "sistema",
            "destinatario": "Todos os usuários",
            "destinatarios": 42,
            "data": "11/08/2026 18:00",
            "lida": True,
            "status": "enviada",
            "icone": "bi-wrench"
        },
        {
            "id": 5,
            "titulo": "Bem-vindo ao Orienta.IA",
            "mensagem": (
                "Sua conta foi criada com sucesso."
            ),
            "tipo": "usuario",
            "destinatario": "Bernardo de Castro",
            "destinatarios": 1,
            "data": "10/08/2026 09:12",
            "lida": True,
            "status": "enviada",
            "icone": "bi-hand-thumbs-up"
        }
    ]

    estatisticas = {
        "total": 128,
        "nao_lidas": 17,
        "enviadas": 112,
        "pendentes": 4
    }

    return render_template("admin/notificacoes.html", notificacoes=notificacoes, estatisticas=estatisticas)

@app.route("/admin/mensagens")
def admin_mensagens():

    conversas = [
        {
            "id": 1,
            "usuario_id": 12,
            "nome": "Ana Carolina Silva",
            "username": "anacarolina",
            "tipo": "Professor",
            "iniciais": "AC",
            "assunto": "Dúvida sobre proposta de projeto",
            "ultima_mensagem": (
                "Gostaria de saber se posso alterar "
                "a descrição do projeto."
            ),
            "data": "12/08/2026 13:18",
            "nao_lidas": 2,
            "online": True
        },
        {
            "id": 2,
            "usuario_id": 18,
            "nome": "Lucas Almeida",
            "username": "lucasalmeida",
            "tipo": "Estudante",
            "iniciais": "LA",
            "assunto": "Solicitação de vínculo",
            "ultima_mensagem": (
                "Enviei minha solicitação de vínculo "
                "com a universidade."
            ),
            "data": "12/08/2026 11:42",
            "nao_lidas": 1,
            "online": False
        },
        {
            "id": 3,
            "usuario_id": 21,
            "nome": "Mariana Oliveira",
            "username": "marianaoliveira",
            "tipo": "Estudante",
            "iniciais": "MO",
            "assunto": "Projeto de iniciação científica",
            "ultima_mensagem": (
                "Obrigado pelo retorno!"
            ),
            "data": "11/08/2026 18:23",
            "nao_lidas": 0,
            "online": True
        },
        {
            "id": 4,
            "usuario_id": 7,
            "nome": "Carlos Henrique",
            "username": "carloshenrique",
            "tipo": "Professor",
            "iniciais": "CH",
            "assunto": "Cronograma do projeto",
            "ultima_mensagem": (
                "O cronograma foi atualizado."
            ),
            "data": "11/08/2026 15:10",
            "nao_lidas": 0,
            "online": False
        },
        {
            "id": 5,
            "usuario_id": 31,
            "nome": "Juliana Mendes",
            "username": "julianamendes",
            "tipo": "Estudante",
            "iniciais": "JM",
            "assunto": "Dúvida sobre candidatura",
            "ultima_mensagem": (
                "Ainda posso me candidatar ao projeto?"
            ),
            "data": "10/08/2026 09:32",
            "nao_lidas": 0,
            "online": False
        }
    ]


    mensagens = {
        1: [
            {
                "id": 1,
                "remetente": "Ana Carolina Silva",
                "iniciais": "AC",
                "mensagem": (
                    "Olá, administrador! Gostaria de saber "
                    "se posso alterar a descrição do meu projeto."
                ),
                "data": "12/08/2026 13:12",
                "propria": False
            },
            {
                "id": 2,
                "remetente": "Administrador",
                "iniciais": "AD",
                "mensagem": (
                    "Olá, Ana! Sim. Você pode solicitar "
                    "a alteração pelo gerenciamento do projeto."
                ),
                "data": "12/08/2026 13:15",
                "propria": True
            },
            {
                "id": 3,
                "remetente": "Ana Carolina Silva",
                "iniciais": "AC",
                "mensagem": (
                    "Perfeito. Vou realizar a alteração. "
                    "Obrigado!"
                ),
                "data": "12/08/2026 13:18",
                "propria": False
            }
        ]
    }


    estatisticas = {
        "total": 36,
        "nao_lidas": 7,
        "enviadas": 24,
        "recebidas": 12
    }


    usuarios = [
        {
            "id": 1,
            "nome": "Bernardo de Castro",
            "email": "bernardo@ufsj.edu.br",
            "tipo": "Estudante"
        },
        {
            "id": 2,
            "nome": "Ana Carolina Silva",
            "email": "ana.silva@ufsj.edu.br",
            "tipo": "Professor"
        },
        {
            "id": 3,
            "nome": "Lucas Almeida",
            "email": "lucas.almeida@ufsj.edu.br",
            "tipo": "Estudante"
        },
        {
            "id": 4,
            "nome": "Mariana Oliveira",
            "email": "mariana.oliveira@ufsj.edu.br",
            "tipo": "Estudante"
        }
    ]


    return render_template("admin/mensagens.html", conversas=conversas, mensagens=mensagens, estatisticas=estatisticas, usuarios=usuarios)
    
# Run
if __name__ == '__main__':
    app.run(debug=True)
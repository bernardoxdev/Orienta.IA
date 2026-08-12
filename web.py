import os

from flask import Flask, render_template, request, redirect
from flask_session import Session

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
    return render_template("dashboard_admin.html", total_usuarios=0, total_estudantes=0, total_professores=0, total_projetos=0, total_candidaturas=0, candidaturas_pendentes=0, propostas_pendentes=0, mensagens_pendentes=0, notificacoes_nao_lidas=0, usuarios_recentes=[], atividades=[], notificacoes=[])
    
@app.route("/admin/usuarios")
def admin_usuarios():
    usuarios = [

        {
            "id": 1,
            "nome": "Bernardo de Castro",
            "username": "bernardocastro",
            "email": "bernardo@ufsj.edu.br",
            "telegram_id": "123456789",
            "role": "user",
            "tipo": "estudante",
            "universidade": "Universidade Federal de São João del-Rei",
            "universidade_sigla": "UFSJ",
            "ativo": True
        },

        {
            "id": 2,
            "nome": "Ana Carolina Silva",
            "username": "anacarolina",
            "email": "ana.silva@ufsj.edu.br",
            "telegram_id": "987654321",
            "role": "user",
            "tipo": "professor",
            "universidade": "Universidade Federal de São João del-Rei",
            "universidade_sigla": "UFSJ",
            "ativo": True
        },

        {
            "id": 3,
            "nome": "Lucas Oliveira",
            "username": "lucasoliveira",
            "email": "lucas.oliveira@ufsj.edu.br",
            "telegram_id": None,
            "role": "user",
            "tipo": "estudante",
            "universidade": "Universidade Federal de São João del-Rei",
            "universidade_sigla": "UFSJ",
            "ativo": True
        },

        {
            "id": 4,
            "nome": "Mariana Souza",
            "username": "marianasouza",
            "email": "mariana@ufmg.br",
            "telegram_id": "456789123",
            "role": "user",
            "tipo": "professor",
            "universidade": "Universidade Federal de Minas Gerais",
            "universidade_sigla": "UFMG",
            "ativo": True
        },

        {
            "id": 5,
            "nome": "Gabriel Santos",
            "username": "gabrielsantos",
            "email": "gabriel@ufsj.edu.br",
            "telegram_id": None,
            "role": "user",
            "tipo": "estudante",
            "universidade": "Universidade Federal de São João del-Rei",
            "universidade_sigla": "UFSJ",
            "ativo": False
        },

        {
            "id": 6,
            "nome": "Juliana Mendes",
            "username": "julianamendes",
            "email": "juliana@ufsj.edu.br",
            "telegram_id": "321654987",
            "role": "user",
            "tipo": "estudante",
            "universidade": "Universidade Federal de São João del-Rei",
            "universidade_sigla": "UFSJ",
            "ativo": True
        },

        {
            "id": 7,
            "nome": "Carlos Eduardo Lima",
            "username": "carloseduardo",
            "email": "carlos@ufop.edu.br",
            "telegram_id": "741852963",
            "role": "user",
            "tipo": "professor",
            "universidade": "Universidade Federal de Ouro Preto",
            "universidade_sigla": "UFOP",
            "ativo": True
        },

        {
            "id": 8,
            "nome": "Rafael Almeida",
            "username": "rafaelalmeida",
            "email": "rafael@ufsj.edu.br",
            "telegram_id": None,
            "role": "user",
            "tipo": "estudante",
            "universidade": "Universidade Federal de São João del-Rei",
            "universidade_sigla": "UFSJ",
            "ativo": True
        },

        {
            "id": 9,
            "nome": "Fernanda Costa",
            "username": "fernandacosta",
            "email": "fernanda@ufmg.br",
            "telegram_id": "159357486",
            "role": "user",
            "tipo": "estudante",
            "universidade": "Universidade Federal de Minas Gerais",
            "universidade_sigla": "UFMG",
            "ativo": True
        },

        {
            "id": 10,
            "nome": "Administrador",
            "username": "admin",
            "email": "admin@orienta.ia",
            "telegram_id": None,
            "role": "admin",
            "tipo": "administrador",
            "universidade": None,
            "universidade_sigla": None,
            "ativo": True
        }

    ]

    return render_template("admin/usuarios.html", usuarios=usuarios)
    
@app.route("/admin/usuarios/novo", methods=["GET", "POST"])
def admin_novo_usuario():
    pass

@app.route(
    "/admin/usuarios/<int:usuario_id>/excluir",
    methods=["POST"]
)
def admin_excluir_usuario(usuario_id):
    pass

@app.route("/admin/usuarios/<int:usuario_id>/editar", methods=["GET", "POST"])
def admin_editar_usuario(usuario_id):
    pass

@app.route("/admin/usuarios/<int:usuario_id>/visualizar")
def admin_visualizar_usuario(usuario_id):
    pass

@app.route("/admin/projetos")
def admin_projetos():
    projetos = [

        {
            "id": 1,
            "titulo": "Inteligência Artificial aplicada à Educação",
            "descricao": "Desenvolvimento de uma plataforma baseada em IA para auxiliar estudantes no processo de aprendizagem.",
            "status": "Em andamento",
            "contexto": "IC",
            "data_inicio": "10/03/2026",
            "data_fim": "10/12/2026",

            "professor": {
                "id": 2,
                "nome": "Ana Carolina Silva",
                "username": "anacarolina"
            },

            "estudante": {
                "id": 1,
                "nome": "Bernardo de Castro",
                "username": "bernardocastro"
            },

            "universidade": {
                "nome": "Universidade Federal de São João del-Rei",
                "sigla": "UFSJ"
            },

            "palavras_chave": [
                "Inteligência Artificial",
                "Educação",
                "Python",
                "LLM"
            ],

            "cronogramas_total": 6,
            "cronogramas_concluidos": 3
        },


        {
            "id": 2,
            "titulo": "Sistema de gerenciamento acadêmico",
            "descricao": "Desenvolvimento de uma aplicação web para gerenciamento de atividades acadêmicas e projetos de pesquisa.",
            "status": "Não iniciado",
            "contexto": "TCC",
            "data_inicio": "01/09/2026",
            "data_fim": "30/06/2027",

            "professor": {
                "id": 3,
                "nome": "Carlos Eduardo Lima",
                "username": "carloseduardo"
            },

            "estudante": {
                "id": 8,
                "nome": "Rafael Almeida",
                "username": "rafaelalmeida"
            },

            "universidade": {
                "nome": "Universidade Federal de Ouro Preto",
                "sigla": "UFOP"
            },

            "palavras_chave": [
                "Web",
                "Sistemas",
                "Banco de Dados"
            ],

            "cronogramas_total": 8,
            "cronogramas_concluidos": 0
        },


        {
            "id": 3,
            "titulo": "Análise de dados educacionais",
            "descricao": "Análise de dados acadêmicos para identificação de padrões de desempenho dos estudantes.",
            "status": "Concluído",
            "contexto": "MESTRADO",
            "data_inicio": "15/02/2025",
            "data_fim": "20/07/2026",

            "professor": {
                "id": 4,
                "nome": "Mariana Souza",
                "username": "marianasouza"
            },

            "estudante": {
                "id": 9,
                "nome": "Fernanda Costa",
                "username": "fernandacosta"
            },

            "universidade": {
                "nome": "Universidade Federal de Minas Gerais",
                "sigla": "UFMG"
            },

            "palavras_chave": [
                "Data Science",
                "Educação",
                "Estatística"
            ],

            "cronogramas_total": 10,
            "cronogramas_concluidos": 10
        },


        {
            "id": 4,
            "titulo": "Middleware para dispositivos RFID",
            "descricao": "Desenvolvimento de middleware para integração e gerenciamento de leitores RFID.",
            "status": "Em andamento",
            "contexto": "IC",
            "data_inicio": "05/04/2026",
            "data_fim": "20/12/2026",

            "professor": {
                "id": 2,
                "nome": "Ana Carolina Silva",
                "username": "anacarolina"
            },

            "estudante": {
                "id": 6,
                "nome": "Juliana Mendes",
                "username": "julianamendes"
            },

            "universidade": {
                "nome": "Universidade Federal de São João del-Rei",
                "sigla": "UFSJ"
            },

            "palavras_chave": [
                "RFID",
                "Java",
                "IoT",
                "Middleware"
            ],

            "cronogramas_total": 7,
            "cronogramas_concluidos": 2
        },


        {
            "id": 5,
            "titulo": "Assistente virtual para orientação acadêmica",
            "descricao": "Criação de um assistente virtual utilizando modelos de linguagem para auxiliar estudantes.",
            "status": "Em andamento",
            "contexto": "TCC",
            "data_inicio": "20/01/2026",
            "data_fim": "15/11/2026",

            "professor": {
                "id": 3,
                "nome": "Carlos Eduardo Lima",
                "username": "carloseduardo"
            },

            "estudante": {
                "id": 3,
                "nome": "Lucas Oliveira",
                "username": "lucasoliveira"
            },

            "universidade": {
                "nome": "Universidade Federal de Ouro Preto",
                "sigla": "UFOP"
            },

            "palavras_chave": [
                "LLM",
                "Python",
                "Telegram",
                "IA"
            ],

            "cronogramas_total": 9,
            "cronogramas_concluidos": 4
        },


        {
            "id": 6,
            "titulo": "Sistema de recomendação de projetos",
            "descricao": "Sistema para recomendar projetos acadêmicos aos estudantes com base em seus interesses.",
            "status": "Não iniciado",
            "contexto": "OUTRO",
            "data_inicio": "01/10/2026",
            "data_fim": "01/05/2027",

            "professor": {
                "id": 4,
                "nome": "Mariana Souza",
                "username": "marianasouza"
            },

            "estudante": None,

            "universidade": {
                "nome": "Universidade Federal de Minas Gerais",
                "sigla": "UFMG"
            },

            "palavras_chave": [
                "Recomendação",
                "Machine Learning",
                "IA"
            ],

            "cronogramas_total": 5,
            "cronogramas_concluidos": 0
        },


        {
            "id": 7,
            "titulo": "Aplicação de visão computacional",
            "descricao": "Estudo da utilização de visão computacional para identificação automática de objetos.",
            "status": "Cancelado",
            "contexto": "IC",
            "data_inicio": "10/02/2026",
            "data_fim": "10/08/2026",

            "professor": {
                "id": 2,
                "nome": "Ana Carolina Silva",
                "username": "anacarolina"
            },

            "estudante": {
                "id": 8,
                "nome": "Rafael Almeida",
                "username": "rafaelalmeida"
            },

            "universidade": {
                "nome": "Universidade Federal de São João del-Rei",
                "sigla": "UFSJ"
            },

            "palavras_chave": [
                "Visão Computacional",
                "Python",
                "OpenCV"
            ],

            "cronogramas_total": 4,
            "cronogramas_concluidos": 1
        }

    ]

    return render_template("admin/projetos.html", projetos=projetos)

@app.route("/admin/candidaturas")
def admin_candidaturas():
    candidaturas = [

        {
            "id": 1,
            "tipo": "candidatura",
            "status": "Pendente",

            "estudante": {
                "id": 1,
                "nome": "Bernardo de Castro",
                "username": "bernardocastro",
                "matricula": "2023001234"
            },

            "projeto": {
                "id": 1,
                "titulo": "Inteligência Artificial aplicada à Educação",
                "contexto": "IC"
            },

            "professor": {
                "id": 2,
                "nome": "Ana Carolina Silva"
            },

            "universidade": {
                "sigla": "UFSJ",
                "nome": "Universidade Federal de São João del-Rei"
            },

            "data": "11/08/2026",
            "mensagem": "Tenho interesse no projeto devido à minha experiência com Python e Inteligência Artificial."
        },


        {
            "id": 2,
            "tipo": "candidatura",
            "status": "Pendente",

            "estudante": {
                "id": 3,
                "nome": "Lucas Oliveira",
                "username": "lucasoliveira",
                "matricula": "2022004567"
            },

            "projeto": {
                "id": 5,
                "titulo": "Assistente virtual para orientação acadêmica",
                "contexto": "TCC"
            },

            "professor": {
                "id": 3,
                "nome": "Carlos Eduardo Lima"
            },

            "universidade": {
                "sigla": "UFOP",
                "nome": "Universidade Federal de Ouro Preto"
            },

            "data": "10/08/2026",
            "mensagem": "Gostaria de participar do desenvolvimento do assistente virtual."
        },


        {
            "id": 3,
            "tipo": "candidatura",
            "status": "Aprovada",

            "estudante": {
                "id": 6,
                "nome": "Juliana Mendes",
                "username": "julianamendes",
                "matricula": "2024007890"
            },

            "projeto": {
                "id": 4,
                "titulo": "Middleware para dispositivos RFID",
                "contexto": "IC"
            },

            "professor": {
                "id": 2,
                "nome": "Ana Carolina Silva"
            },

            "universidade": {
                "sigla": "UFSJ",
                "nome": "Universidade Federal de São João del-Rei"
            },

            "data": "08/08/2026",
            "mensagem": "Tenho interesse em sistemas embarcados, IoT e RFID."
        },


        {
            "id": 4,
            "tipo": "candidatura",
            "status": "Recusada",

            "estudante": {
                "id": 8,
                "nome": "Rafael Almeida",
                "username": "rafaelalmeida",
                "matricula": "2021006543"
            },

            "projeto": {
                "id": 2,
                "titulo": "Sistema de gerenciamento acadêmico",
                "contexto": "TCC"
            },

            "professor": {
                "id": 3,
                "nome": "Carlos Eduardo Lima"
            },

            "universidade": {
                "sigla": "UFOP",
                "nome": "Universidade Federal de Ouro Preto"
            },

            "data": "05/08/2026",
            "mensagem": "Tenho experiência no desenvolvimento de aplicações web."
        },


        {
            "id": 5,
            "tipo": "cancelamento",
            "status": "Pendente",

            "estudante": {
                "id": 9,
                "nome": "Fernanda Costa",
                "username": "fernandacosta",
                "matricula": "2020003210"
            },

            "projeto": {
                "id": 3,
                "titulo": "Análise de dados educacionais",
                "contexto": "MESTRADO"
            },

            "professor": {
                "id": 4,
                "nome": "Mariana Souza"
            },

            "universidade": {
                "sigla": "UFMG",
                "nome": "Universidade Federal de Minas Gerais"
            },

            "data": "09/08/2026",

            "origem": "Estudante",

            "mensagem": "Solicito o cancelamento do projeto devido à impossibilidade de continuar participando."
        },


        {
            "id": 6,
            "tipo": "cancelamento",
            "status": "Pendente",

            "estudante": {
                "id": 3,
                "nome": "Lucas Oliveira",
                "username": "lucasoliveira",
                "matricula": "2022004567"
            },

            "projeto": {
                "id": 5,
                "titulo": "Assistente virtual para orientação acadêmica",
                "contexto": "TCC"
            },

            "professor": {
                "id": 3,
                "nome": "Carlos Eduardo Lima"
            },

            "universidade": {
                "sigla": "UFOP",
                "nome": "Universidade Federal de Ouro Preto"
            },

            "data": "07/08/2026",

            "origem": "Professor",

            "mensagem": "Solicito o cancelamento devido à alteração no planejamento do projeto."
        }

    ]

    return render_template("admin/candidaturas.html", candidaturas=candidaturas)

@app.route("/admin/propostas")
def admin_propostas():
    propostas = [

        {
            "id": 1,

            "titulo": "Sistema de recomendação de projetos acadêmicos",

            "descricao": (
                "Desenvolvimento de um sistema capaz de recomendar "
                "projetos de pesquisa aos estudantes utilizando técnicas "
                "de inteligência artificial e análise de interesses."
            ),

            "estudante": {
                "id": 1,
                "nome": "Bernardo de Castro",
                "username": "bernardocastro",
                "matricula": "2023001234"
            },

            "universidade": {
                "id": 1,
                "nome": "Universidade Federal de São João del-Rei",
                "sigla": "UFSJ"
            },

            "contexto": "IC",

            "area": "Inteligência Artificial",

            "palavras_chave": [
                "IA",
                "Machine Learning",
                "Recomendação",
                "Python"
            ],

            "status": "Pendente",

            "data": "11/08/2026",

            "observacao": (
                "Gostaria de desenvolver o projeto utilizando "
                "modelos de recomendação e LLMs."
            )
        },


        {
            "id": 2,

            "titulo": "Plataforma de gerenciamento de laboratórios",

            "descricao": (
                "Criação de uma plataforma web para gerenciamento "
                "de equipamentos, reservas e usuários dos laboratórios "
                "da universidade."
            ),

            "estudante": {
                "id": 3,
                "nome": "Lucas Oliveira",
                "username": "lucasoliveira",
                "matricula": "2022004567"
            },

            "universidade": {
                "id": 1,
                "nome": "Universidade Federal de São João del-Rei",
                "sigla": "UFSJ"
            },

            "contexto": "TCC",

            "area": "Engenharia de Software",

            "palavras_chave": [
                "Web",
                "Python",
                "PostgreSQL",
                "React"
            ],

            "status": "Pendente",

            "data": "10/08/2026",

            "observacao": (
                "A proposta busca solucionar problemas encontrados "
                "no gerenciamento dos laboratórios."
            )
        },


        {
            "id": 3,

            "titulo": "Análise de desempenho acadêmico",

            "descricao": (
                "Estudo de técnicas de análise de dados para identificar "
                "padrões de desempenho acadêmico e fatores relacionados "
                "ao rendimento dos estudantes."
            ),

            "estudante": {
                "id": 9,
                "nome": "Fernanda Costa",
                "username": "fernandacosta",
                "matricula": "2020003210"
            },

            "universidade": {
                "id": 2,
                "nome": "Universidade Federal de Minas Gerais",
                "sigla": "UFMG"
            },

            "contexto": "MESTRADO",

            "area": "Ciência de Dados",

            "palavras_chave": [
                "Data Science",
                "Estatística",
                "Educação"
            ],

            "status": "Em análise",

            "data": "08/08/2026",

            "observacao": (
                "Pretendo utilizar dados históricos para identificar "
                "padrões de desempenho."
            )
        },


        {
            "id": 4,

            "titulo": "Middleware para integração de dispositivos RFID",

            "descricao": (
                "Desenvolvimento de uma camada de middleware capaz "
                "de integrar diferentes leitores RFID e disponibilizar "
                "uma API padronizada."
            ),

            "estudante": {
                "id": 6,
                "nome": "Juliana Mendes",
                "username": "julianamendes",
                "matricula": "2024007890"
            },

            "universidade": {
                "id": 1,
                "nome": "Universidade Federal de São João del-Rei",
                "sigla": "UFSJ"
            },

            "contexto": "IC",

            "area": "Internet das Coisas",

            "palavras_chave": [
                "RFID",
                "Java",
                "IoT",
                "API"
            ],

            "status": "Aprovada",

            "data": "02/08/2026",

            "observacao": (
                "Projeto voltado para integração de leitores "
                "RFID de diferentes fabricantes."
            )
        },


        {
            "id": 5,

            "titulo": "Aplicação de visão computacional para laboratórios",

            "descricao": (
                "Desenvolvimento de uma aplicação utilizando visão "
                "computacional para identificação automática de objetos."
            ),

            "estudante": {
                "id": 8,
                "nome": "Rafael Almeida",
                "username": "rafaelalmeida",
                "matricula": "2021006543"
            },

            "universidade": {
                "id": 1,
                "nome": "Universidade Federal de São João del-Rei",
                "sigla": "UFSJ"
            },

            "contexto": "IC",

            "area": "Visão Computacional",

            "palavras_chave": [
                "OpenCV",
                "Python",
                "IA"
            ],

            "status": "Recusada",

            "data": "28/07/2026",

            "observacao": (
                "A proposta foi considerada fora da área dos "
                "professores disponíveis atualmente."
            )
        }

    ]

    return render_template("admin/propostas.html", propostas=propostas)

@app.route("/admin/universidades")
def admin_universidades():
    pass

@app.route("/admin/configuracoes")
def admin_configuracoes():
    pass

@app.route("/admin/dados")
def admin_dados():
    pass

@app.route("/admin/notificoes")
def admin_notificacoes():
    pass

@app.route("/admin/mensagens")
def admin_mensagens():
    pass

# Run
if __name__ == '__main__':
    app.run(debug=True)
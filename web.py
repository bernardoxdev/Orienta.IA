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
    return render_template("dashboard_professor.html")

@app.route("/logout")
def logout():
    pass

@app.route("/forgot-password")
def forgot_password():
    pass

# Run
if __name__ == '__main__':
    app.run(debug=True)
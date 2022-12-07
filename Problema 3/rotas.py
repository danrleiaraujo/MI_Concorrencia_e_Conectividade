from flask import Flask, render_template, request
from static.usuarios import *
import ast

app = Flask(__name__)

# ---------------------------------------
#Pagina inicial
@app.route("/",  methods = ['GET'])
def index():
    return render_template ('index.html')

# ---------------------------------------
#Página de login
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #Recebimento de dados:
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    verifica = verificaUser(usuario, senha)
    if(verifica):
        return logado(usuario, senha)
    return render_template ('login.html')

# ---------------------------------------
#Página de logado
@app.route("/logado/<adm>/<senha>", methods = ['GET'])
def logado(adm, senha):
    verifica = verificaUser(adm, senha)
    if(verifica):
        return render_template ('indexLogado.html', user = adm)
    else:
        return login()

app.run(debug=True)
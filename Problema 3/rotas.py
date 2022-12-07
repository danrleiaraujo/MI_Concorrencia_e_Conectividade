from flask import Flask, render_template, request, url_for, redirect
from static.usuarios import *

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
    l ="http://127.0.0.1:5000/logado/" + str(usuario) + "/" + str(senha)
    if(verifica):
        return redirect(l)
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
# --------------------------------------- IMPORTs ----------------------------------------  
from flask import Flask, render_template, request, url_for, redirect
from static.usuarios import *
from static.produtosOfertados import *
import json

app = Flask(__name__)

# --------------------------------------- ROUTS ----------------------------------------  
#Pagina inicial
@app.route("/",  methods = ['GET'])
def index():
    return render_template ('index.html')

# --------------------------------------------------------------------------------------------
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

# --------------------------------------------------------------------------------------------
#Página de logado
@app.route("/logado/<adm>/<senha>/", methods = ['GET'])
def logado(adm, senha):
    verifica = verificaUser(adm, senha)
    if(verifica):
        return render_template ('indexLogado.html', user = adm, s = senha)
    else:
        return login()

# --------------------------------------------------------------------------------------------
#Página de cadastro do adm
@app.route("/logado/<adm>/<senha>/novoAdm", methods = ['GET', 'POST'])
def novo_Adm(adm, senha):
    verifica = verificaUser(adm, senha)
    if(verifica):
        novo_usuario = request.form.get('usuario')
        nova_senha = request.form.get('senha')
        if(type(novo_usuario) != None or type(nova_senha) != None ):
            result = adicionarAdm(novo_usuario, nova_senha)
        if(result):
            sucess = "Cadastrado com sucesso!"
            return render_template ('logadoNovoAdm.html', sucesso = sucess, user = adm, s = senha)
        return render_template ('logadoNovoAdm.html', user = adm, s = senha)
    else:
        return login()

# --------------------------------------------------------------------------------------------
#Página de cadastro de produto
@app.route("/logado/<adm>/<senha>/novoProduto", methods = ['GET', 'POST'])
def novo_Produto(adm, senha):    
    verifica = verificaUser(adm, senha)
    if(verifica):
        novo_nome = request.form.get('nome')
        nova_quantidade = request.form.get('quantidade')   
        novo_descricao = request.form.get('descricao')
        nova_preco = request.form.get('preco')
        result = adicionar_produtos(novo_nome, nova_quantidade, novo_descricao, nova_preco)
        if(result):
            sucess = "Cadastrado com sucesso!"
            return render_template ('logadoNovoProduto.html', sucesso = sucess, user = adm, s = senha)
        return render_template ('logadoNovoProduto.html', user = adm, s = senha)
    else:
        return login()

# ------------------------------------------------------------------------------------
#Página de verifiçaão de adm
@app.route("/logado/<adm>/<senha>/verAdm", methods = ['GET'])
def ver_Adm(adm, senha):    
    verifica = verificaUser(adm, senha)
    if(verifica):
        adms = getAdm()
        print(type(adms))
        print(adms)
        return render_template ('logadoverProduto.html', user = adm, s = senha, adm = adms )
        
# ----------------------------------------------------------------------------------------
#Página verifiçaão de produtos
@app.route("/logado/<adm>/<senha>/verProduto", methods = ['GET'])
def ver_Produto(adm, senha):    
    verifica = verificaUser(adm, senha)
    if(verifica):
        produtos = get_produtos_ofertados()
        print(type(produtos))
        print(produtos)
        return render_template ('logadoverProduto.html', user = adm, s = senha, produtos = produtos)

# --------------------------------------- RUN ----------------------------------------   
app.run(debug=True)
# ------------------------------------------------------------------------------------ 
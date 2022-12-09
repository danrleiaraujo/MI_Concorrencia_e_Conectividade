# --------------------------------------- IMPORTs ----------------------------------------  
from flask import Flask, render_template, request, redirect
from static.usuarios import *
from static.produtosOfertados import *

app = Flask(__name__)

# --------------------------------------- ROUTS ----------------------------------------  
#Pagina inicial
@app.route("/",  methods =['GET', 'POST'])
def index():
    id_loja = request.form.get('idLoja')
    nome = request.form.get('nome')
    quantidade= request.form.get('nome')
    
    if (request.form.get('quantidade') != None):        
        id_loja = request.form.get('idLoja')
        nome = request.form.get('nome')
        quantidade = request.form.get('quantidade')
        novocarrinho(id_loja, nome, quantidade)
    produtos_carrinho = getcarrinho()
    produtos = get_produtos_ofertados()
    return render_template ('index.html', produtos = produtos, produtos_carrinho = produtos_carrinho)
    
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
        return redirect("http://127.0.0.1:5000/login")

# --------------------------------------------------------------------------------------------
#Página de cadastro do adm
@app.route("/logado/<adm>/<senha>/novoAdm", methods = ['GET', 'POST'])
def novo_adm(adm, senha):
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
        return redirect("http://127.0.0.1:5000/login")

# --------------------------------------------------------------------------------------------
#Página de cadastro de produto
@app.route("/logado/<adm>/<senha>/novoProduto", methods = ['GET', 'POST'])
def novo_produto(adm, senha):    
    verifica = verificaUser(adm, senha)
    if(verifica):
        novo_id = request.form.get('idLoja')
        novo_nome = request.form.get('nome')
        nova_quantidade = request.form.get('quantidade')  
        novo_descricao = request.form.get('descricao')
        nova_preco = request.form.get('preco')
        if(nova_quantidade != None): 
            nova_quantidade = int(nova_quantidade)
        result = adicionar_produtos(novo_id, novo_nome, nova_quantidade, novo_descricao, nova_preco)
        if(result):
            sucess = "Cadastrado com sucesso!"
            return render_template ('logadoNovoProduto.html', sucess = sucess, user = adm, s = senha)
        return render_template ('logadoNovoProduto.html', user = adm, s = senha)
    else:
        return redirect("http://127.0.0.1:5000/login")

# ------------------------------------------------------------------------------------
#Página de verifição de adm
@app.route("/logado/<adm>/<senha>/verAdm", methods = ['GET'])
def ver_adm(adm, senha):    
    verifica = verificaUser(adm, senha)
    if(verifica):
        adms = getAdm()
        return render_template ('logadoverAdm.html', user = adm, s = senha, adms = adms )    
    else:
        return redirect("http://127.0.0.1:5000/login")
        
# ----------------------------------------------------------------------------------------
#Página verifição de produtos
@app.route("/logado/<adm>/<senha>/verProduto", methods = ['GET'])
def ver_produto(adm, senha):    
    verifica = verificaUser(adm, senha)
    if(verifica):
        produtos = get_produtos_ofertados()
        return render_template ('logadoVerProduto.html', user = adm, s = senha, produtos = produtos)
    else:
         return redirect("http://127.0.0.1:5000/login")
# --------------------------------------------------------------------------------------------
#Página de remoção de produto
@app.route("/logado/<adm>/<senha>/removerProduto", methods = ['GET', 'POST'])
def remover_produto(adm, senha):    
    verifica = verificaUser(adm, senha)
    if(verifica):
        id = request.form.get('idLoja')
        nome = request.form.get('nome')
        quantidade = request.form.get('quantidade')   
        if(quantidade != None): 
            quantidade = int(quantidade)
        result = remover_produtos(id, nome, quantidade)
        if(result):
            sucess = "Removido com sucesso!"
            return render_template ('logadoRemoverProduto.html', sucesso = sucess, user = adm, s = senha)
        return render_template ('logadoRemoverProduto.html', user = adm, s = senha)
    else:
        return redirect("http://127.0.0.1:5000/login")

# ------------------------------------------------------------------------------------
#Página de remoção de adm
@app.route("/logado/<adm>/<senha>/removerAdm", methods = ['GET', 'POST'])
def remover_adm(adm, senha):    
    verifica = verificaUser(adm, senha)
    if(verifica):
        novo_nome = request.form.get('usuario')
        result = removerUser(novo_nome)
        if(result):
            sucess = "Removido com sucesso!"
            return render_template ('logadoRemoverAdm.html', sucesso = sucess, user = adm, s = senha)
        return render_template ('logadoRemoverAdm.html', user = adm, s = senha)
    else:
        return redirect("http://127.0.0.1:5000/login")

# ------------------------------------------------------------------------------------
# --------------------------------------- RUN ----------------------------------------   
app.run(debug=True)
# ------------------------------------------------------------------------------------ 
#inicio de um dicionário para os produtos
produtos_ofertados = {
    "bahia123":{
        "nome" : "Blusa", 
        "quantidade" : 3, 
        "desc_produto": "Blusa Preta", 
        "preco_produto" : 16.78
    }
}

#Função para adicionar um produto ofertado.
def adicionar_produtos(id, nome, qtd, descricao, preco):
    if(id == "" or nome == "" or qtd == "" or descricao == "" or preco == ""):
        return False
    if(id == None or nome ==  None or qtd == None or descricao == None or preco == None):
        return False
    global produtos_ofertados
    #Criação do produto:
    produto = {"nome" : nome, "quantidade" : qtd, "desc_produto": descricao, "preco_produto" : preco}
    #Salva o produto e sua quantidade no dicionário de produtos ofertados.
    produtos_ofertados[id] = produto
    if nome in produtos_ofertados.keys():
        return True;
    else:
        return False;

#Função para remover certa quantidade do produto.
def remover_produtos(id, nome, qtd):
    global produtos_ofertados
    #Caso exista o nome nos produtos ofertados
    if nome in produtos_ofertados:
        # Recebe o produto para possível modificação:
        produto = produtos_ofertados.get(nome)
        # Recebe a quantidade do produto para possível modificação:
        quantidade = produto["quantidade"]
        #Faz a subtração da quantidade anterior pela quantidade passada:
        quantidade = quantidade - qtd
        #Se a quantidade resultar a zero, retira o produto da lista de ofertados
        if quantidade == 0:
            produtos_ofertados.pop(nome)
        #Caso ainda sobre algo:
        elif(quantidade > 0):
            produto["quantidade"] = quantidade
        #Caso tente tirar mais do que tem em estoque:
        else:
            print("O máximo que temos é: ", produto["quantidade"])
    #Caso NÃO exista o nome nos produtos ofertados
    else:
        print("Não temos este produto em estoque")


def get_produtos_ofertados():
    global produtos_ofertados
    return produtos_ofertados

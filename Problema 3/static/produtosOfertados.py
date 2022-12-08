#inicio de um dicionário para os produtos

carrinho = {}
produtos_ofertados = {
    "bahia123":{
        "blusa":{
            "quantidade" : 5, 
            "desc_produto": "Blusa Preta", 
            "preco_produto" : 16.78
        },
        "short":{
            "quantidade" : 3, 
            "desc_produto": "short Preta", 
            "preco_produto" : 20.78
        }         ,
        "vestido":{
            "quantidade" : 2, 
            "desc_produto": "Vestido Preto", 
            "preco_produto" : 100
        } 
    },    
    "Bahia":{
        "blusa":{
            "quantidade" : 9, 
            "desc_produto": "Blusa Preta", 
            "preco_produto" : 20
        },
        "camisa":{
            "quantidade" : 4, 
            "desc_produto": "Camisa Preta", 
            "preco_produto" : 17
        } 
    }
}

#verifica se existe a chave
def checkKey(dict, key): 
    if key in dict.keys(): 
        return True
    else: 
        return False

def carrinho(id_loja, nome, quantidade):
    global carrinho
    if id_loja in carrinho:
        carrinho[id_loja].update(quantidade, quantidade)
    carrinho[id_loja] ={'nome':nome, "quantidade":quantidade}


#Função para adicionar um produto ofertado.
def adicionar_produtos(id, nome, qtd, descricao, preco):
    if(id == "" or nome == "" or qtd == "" or descricao == "" or preco == ""):
        return False
    if(id == None or nome ==  None or qtd == None or descricao == None or preco == None):
        return False
    global produtos_ofertados
    #Se existir a loja nos produtos ofertados:
    if id in produtos_ofertados.keys():
        #Se existir o produto na loja:
        if nome in produtos_ofertados[id].keys():
            # Recebe o produto para possível modificação:
            produto = produtos_ofertados[id].get(nome)

            # Recebe a quantidade do produto para possível modificação:
            quantidade = produto.get('quantidade')

            #Faz a adicao da quantidade anterior pela quantidade passada:
            quantidade = quantidade + qtd

            # Coloca a nova quantidade
            produto["quantidade"] = quantidade

            #Salva o produto com a nova quantidade
            produtos_ofertados[id].fromkeys((nome), produto)
            return True
        else:
            #Criação do produto
            produto = { nome: { "quantidade" : qtd, "desc_produto": descricao, "preco_produto" : preco}}
            #Salva o produto e sua quantidade no dicionário de produtos ofertados.
            produtos_ofertados[id].update(produto)
    else:
        #Criação do produto
        produto = { nome: { "quantidade" : qtd, "desc_produto": descricao, "preco_produto" : preco}}
        #Cria a loja com o produto.
        produtos_ofertados[id] = produto

#Função para remover certa quantidade do produto.
def remover_produtos(id, nome, qtd):
    global produtos_ofertados
    #Caso exista o nome nos produtos ofertados
    if id in produtos_ofertados:
        if nome in produtos_ofertados[id].keys():
            # Recebe o produto para possível modificação:
            produto = produtos_ofertados[id].get(nome)
            # Recebe a quantidade do produto para possível modificação:
            quantidade = produto.get('quantidade')

            #Faz a subtração da quantidade anterior pela quantidade passada:
            quantidade = quantidade - qtd
            #Se a quantidade resultar a zero, retira o produto da lista de ofertados
            if quantidade == 0:
                produtos_ofertados[id].pop(nome)
                return True
            #Caso ainda sobre algo:
            elif(quantidade > 0):
                produto["quantidade"] = quantidade
                produtos_ofertados[id].fromkeys((nome), produto)
                return True
            #Caso tente tirar mais do que tem em estoque:
            else:
                print("O máximo que temos é: ", produto["quantidade"])
                return False

        #Caso NÃO exista o nome nos produtos ofertados
        else:
            return False;


def get_produtos_ofertados():
    global produtos_ofertados
    return produtos_ofertados

'''def run():
    adicionar_produtos("Bahia","Blusa", 2,"Blusa de frio", 2.50)
    print("Produto adicionado")
    print(get_produtos_ofertados())
    print()

    remover_produtos("Bahia","Blusa", 1)
    print("Produto removido")
    print(get_produtos_ofertados())
    print()

    adicionar_produtos("bahia123","camisa", 4,"Blusa de frio", 2.50)
    print("Produto adicionado")
    print(get_produtos_ofertados())

run()
'''
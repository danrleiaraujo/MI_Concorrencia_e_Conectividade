#inicio de um dicionário para os produtos
produtos_ofertados = {}

#Função para adicionar um produto ofertado.
def adicionar_produtos(nome, qtd, descricao, preco):
    global produtos_ofertados
    #Criação do produto:
    produto = {"quantidade" : qtd, "desc_produto": descricao, "preco_produto" : preco}
    #Salva o produto e sua quantidade no dicionário de produtos ofertados.
    produtos_ofertados[nome] = produto

#Função para remover certa quantidade do produto.
def remover_produtos(nome, qtd):
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

def run():
    ''' ----------- TESTE ------------------------ '''
    adicionar_produtos("blusa", 2, "moletom de algodão", 18.6)
    print (get_produtos_ofertados())
    remover_produtos("blusa", 1)
    print (get_produtos_ofertados())

run()
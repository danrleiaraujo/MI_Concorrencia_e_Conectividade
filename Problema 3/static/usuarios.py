adm = {   
    1:{
        "nome": "Danrlei_Araujo",
        "senha": "1010"
    },
    2:{
        "nome": "Evelyn_Suzart",
        "senha": "1212"
    }
}

#Retorna a lista:
def getAdm():
    global adm
    lista_adm = adm
    return lista_adm

#Adiciona:
def adicionarAdm(usuario, senha):
    global adm
    final = len(adm) + 1 
    novo = {"nome":usuario, "senha":senha}
    adm[final] = novo

#Verifica se existe:
def verificaUser(usuario, senha):
    global adm
    administradores = getAdm()
    for user in administradores:
        admin = administradores.get(user)
        if(usuario == admin.get("nome") and senha == admin.get("senha")):
            return True
    return False
    #Caso contrário:

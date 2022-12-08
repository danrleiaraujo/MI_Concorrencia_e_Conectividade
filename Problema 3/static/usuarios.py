adm = {   
    1:{
        "nome": "Danrlei_Araujo",
        "senha": "1010"
    },
    2:{
        "nome": "Evelyn_Suzarte",
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
    if(usuario == None or senha == None):
        return False
    if(usuario == "" or senha == ""):
        return False
    global adm
    key =0
    while(checkKey(adm, key)):
        key = key + 1
    novo = {"nome":usuario, "senha":senha}
    adm[key] = novo
    return True

#Verifica se existe:
def verificaUser(usuario, senha):
    global adm
    administradores = getAdm()
    for user in administradores:
        admin = administradores.get(user)
        if(usuario == admin.get("nome") and senha == admin.get("senha")):
            return True
    #Caso contrário:
    return False

#verifica se existe a chave
def checkKey(dict, key): 
    if key in dict.keys(): 
        return True
    else: 
        return False 

#exclui:
def removerUser(usuario):
    if(usuario == None ):
        return False
    if(usuario == ""):
        return False
    global adm
    administradores = getAdm()
    for user in administradores:
        admin = administradores.get(user)
        if(usuario == admin.get("nome")):
            u = int(user)
    administradores.pop(u)
    return True

class Clientes:
    def __init__(self, nome, endereco, senha):
        self.nome = nome
        self.endereco= endereco
        self.senha= senha
    #--------------------------------------------------------
    def getNome(self):
        return self.nome

    def getSenha(self):
        return self.senha

    def getEndereco(self):
        return self.endereco
    #---------------------------------------------------------
    def setNome(self, nome):
        self.nome = nome

    def getSenha(self,senha):
        self.senha = senha

    def setEndereco(self,endereco):
        self.endereco = endereco    
    #--------------------------------------------------
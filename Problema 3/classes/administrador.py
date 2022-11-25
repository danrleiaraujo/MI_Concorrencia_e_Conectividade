class Administrador:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha= senha
    #--------------------------------------------------------
    def getNome(self):
        return self.nome

    def getSenha(self):
        return self.senha
    #---------------------------------------------------------
    def setNome(self, nome):
        self.nome = nome

    def getSenha(self,senha):
        self.nome = senha
    #--------------------------------------------------
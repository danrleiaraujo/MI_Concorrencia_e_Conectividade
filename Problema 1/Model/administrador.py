class Administrador:
    def __init__(self, nome, matricula, senha):
        self.nome = nome
        self.matricula = matricula
        self.senha= senha
    #--------------------------------------------------------
    def getNome(self):
        return self.nome

    def getSenha(self):
        return self.senha

    def getMatricula(self):
        return self.matricula
    #---------------------------------------------------------
    def setNome(self, nome):
        self.nome = nome

    def getSenha(self,senha):
        self.nome = senha

    def setMatricula(self,matricula):
        self.nome = matricula
    #--------------------------------------------------
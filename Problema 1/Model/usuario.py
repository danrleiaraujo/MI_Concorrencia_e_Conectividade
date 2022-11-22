class Usuario:
    def __init__(self, nome, matricula, statusConta, endereco, senha, conta):
        self.nome = nome
        self.senha= senha
        self.matricula = matricula
        self.statusConta= statusConta
        self.endereco= endereco
    #--------------------------------------------------------
    def getNome(self):
        return self.nome

    def getSenha(self):
        return self.senha

    def getMatricula(self):
        return self.matricula
        
    def getStatusConta(self):
        return self.statusConta

    def getEndereco(self):
        return self.endereco

    #---------------------------------------------------------
    def setNome(self, nome):
        self.nome = nome

    def getSenha(self,senha):
        self.senha = senha

    def setMatricula(self,matricula):
        self.matricula = matricula
        
    def setStatusConta(self,statusConta):
         self.statusConta = statusConta

    def setEndereco(self,endereco):
        self.endereco = endereco    
    #--------------------------------------------------
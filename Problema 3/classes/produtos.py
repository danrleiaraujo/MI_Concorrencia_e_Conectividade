class Produtos:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
    #--------------------------------------------------------
    def getNome(self):
        return self.nome

    def getDescricao(self):
        return self.descricao
    #---------------------------------------------------------
    def setNome(self, nome):
        self.nome = nome

    def getDescricao(self,descricao):
        self.descricao = descricao
    #--------------------------------------------------
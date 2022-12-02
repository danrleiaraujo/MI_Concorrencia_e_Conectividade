class MarketPlace():
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.bancoDados = {}
    #--------------------------------------------------------------------
    ''' Bloco de Get '''
    def getID(self):
        return self.id

    def getNome(self):
        return self.nome

    def getBancoDados(self):
        return self.bancoDados

    #--------------------------------------------------------------------
    ''' Bloco de Set '''
    def setID(self, id):
        self.id = id

    def setNome(self, nome):
        self.nome = nome

    def setBancoDados(self, bancoDados):
        self.bancoDados = bancoDados

 
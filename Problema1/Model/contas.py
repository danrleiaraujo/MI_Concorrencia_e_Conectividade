class Contas:
    def __init__(self, matricula, data, valor, consumo, status_pagamento):
        self.matricula = matricula
        self.data = data
        self.valor = valor
        self.consumo = consumo
        self.status_pagamento = status_pagamento
    #--------------------------------------------------------
    def getData(self):
        return self.data
    
    def getValor(self):
        return self.valor

    def getConsumo(self):
        return self.consumo

    def getPagamento(self):
        return self.status_pagamento

    #--------------------------------------------------------

    def setData(self, data):
        self.data = data
    
    def setValor(self, valor):
        self.valor = valor

    def setConsumo(self, consumo):
        self.consumo = consumo

    def setPagamento(self, status_pagamento):
        self.status_pagamento = status_pagamento
 
    #--------------------------------------------------------       

    def calcularValor(self,consumo):
        valorTotal = 3.14 * consumo
        return valorTotal
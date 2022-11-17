class Hidrometro():
    def __init__(self, matricula, contaPaga, funcionamento, vazao, vazamento, valorMax):
        #identificação
        self.matricula = matricula;
        #funcionamento
        self.contaPaga = contaPaga;
        self.funcionamento= funcionamento;
        self.consumo= 0;
        #vazamento
        self.vazao= vazao;
        self.vazamento = vazamento;
        self.vazaoPadrao = 3;
        self.valorMax = valorMax;
    #--------------------------------------------------------------------
    ''' Bloco de Get '''
    def getMatricula(self):
        return self.matricula;

    def getContaPaga(self):
        return self.contaPaga;

    def getStatus(self):
        return self.funcionamento;
        
    def getConsumo(self):
        return self.consumo;

    def getVazao(self):
        return self.vazao;

    def getVazamento(self):
        return self.vazamento;

    def getVazaoPadrao(self):
        return self.vazaoPadrao;

    def getValorMax(self):
        return self.valorMax;

    #--------------------------------------------------------------------
    ''' Bloco de Set '''
    def setMatricula(self, matricula):
        self.matricula = matricula;

    def setContaPaga(self, contaPaga):
        self.contaPaga = contaPaga;

    def setConsumo(self, consumo):
        self.consumo = consumo;

    def setVazao(self, vazao):
        self.vazao= vazao;

    def setVazamento(self, vazamento):
        self.vazamento = vazamento;
        
    def setVazaoPadrao(self, vazaoPadrao):
        self.vazaoPadrao = vazaoPadrao;
    
    def setValorMax(self, valorMax):
        self.valorMax = valorMax;
    #---------------------------------------------------------------------------------
    ''' ---------------------------------Funções--------------------------------- '''
    #Função que sinaliza que há vazamento
    def vazamentos(self):
        if (self.vazao > self.vazaoPadrao):
            self.vazamento = True;
            return True
        else:
            self.vazamento = False;
            return False    

    #Função para ativar ou desativar o hidrometro
    def novoStatus(self, status):
        if status == True: self.funcionamento = True;
        else: self.funcionamento = False;

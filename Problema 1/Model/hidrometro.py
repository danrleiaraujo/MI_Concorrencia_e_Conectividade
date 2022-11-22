class Hidrometro():
    def __init__(self, matricula, endereco, funcionamento, vazao, consumo, vazamento):
        #identificação
        self.matricula = matricula;
        self.endereco= endereco;
        #funcionamento
        self.funcionamento= funcionamento;
        self.consumo= consumo;
        #vazamento
        self.vazao= vazao;
        self.vazamento = vazamento;
        self.vazaoPadrao = 3;
    #--------------------------------------------------------------------
    ''' Bloco de Get '''
    def getMatricula(self):
        return self.matricula;

    def getEndereco(self):
        return self.endereco;

    def getStatus(self):
        return self.funcionamento;
        
    def getConsumo(self):
        return self.consumo;

    def getVazao(self):
        return self.vazao;

    def getVazamento(self):
        return self.vazamento;
    #--------------------------------------------------------------------
    ''' Bloco de Set '''
    def setMatricula(self, matricula):
        self.matricula = matricula;

    def setEndereco(self,endereco):
        self.endereco = endereco;

    def setConsumo(self, consumo):
        self.consumo = consumo;

    def setVazao(self, vazao):
        self.vazao= vazao;

    def setVazamento(self, vazamento):
        self.vazamento = vazamento;
    #---------------------------------------------------------------------------------
    ''' Funções '''
    #função que sinaliza que há vazamento
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
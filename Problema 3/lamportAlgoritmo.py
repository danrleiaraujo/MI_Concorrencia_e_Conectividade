import signal
import sys
import time
import threading
import queue

processo_inicial = "A"
procs = {"A", "B", "C"}
eventos_counts = {"A": 2, "B": 0, "C": 0}
fila_mensagens = {"A" : queue.Queue(), "B": queue.Queue(), "C": queue.Queue()}

#criação de mensagem
class Mensagem(object):
    def __init__(self, msg, rotulo_data, emissor, receptor):
        self.msg = msg
        self.rotulo_data = rotulo_data
        self.emissor = emissor
        self.receptor = receptor

    def __repr__(self):
        return "Mensagem {} em {} de {} a {}".format(
        	self.msg, self.rotulo_data, 
        	self.emissor, self.receptor)

class Processo(threading.Thread):

    def __init__(self, nome, concedido, outrosProcessos):
        super(Processo, self).__init__()
        self.nome = nome
        self.temRecurso = concedido == nome
        self.outrosProcessos = outrosProcessos
        self.lamport_clock = 0 # tick after each "event"
        self.requisicoes_fila = []
        self.pedido = False
        self.requisicoes_fila.append(Mensagem("request", 
        	-1, concedido, concedido))

    #remove requisição da fila
    def removerRequisicao(self, msg, emissor):
        index_req = -1
        for i in range(len(self.requisicoes_fila)):
            if self.requisicoes_fila[i].msg == msg and \
               self.requisicoes_fila[i].emissor == emissor:
                index_req = i
                break
        if i == -1:
            print("Não foi possível remover") 
        else:
            del self.requisicoes_fila[i]

    #usar recurso solicitado
    def usarRecurso(self):
        print("Processo {} está usando recurso".format(self.nome))
        eventos_counts[self.nome] += 1
        time.sleep(2)

    #ação de acordo com a mensagem de ação recebida
    def processandoMsg(self, msg):
        #coloca na fila de requisição e envia um "ack" ao emissor
        # como forma de indicar que recebeu a solicitação
        if msg.msg == "request":
            self.requisicoes_fila.append(msg)
            for proc in self.outrosProcessos:
                if proc == msg.emissor:
                    fila_mensagens[proc].put(Mensagem(
                    	"ack", self.lamport_clock, 
                    	self.nome, msg.emissor))
        #tem um outro lançamento, remove essa solicitação da fila                
        elif msg.msg == "release":
            self.removerRequisicao("request", msg.emissor)
        elif msg.msg == "ack":
            pass
        else:
            print("Tipo de mensagem desconhecido!!")

    def run(self):
        while True:
            if self.temRecurso:
                self.usarRecurso()
                self.removerRequisicao("request", self.nome)
                # Diz a todos que concluiu
                for proc in self.outrosProcessos:
                    fila_mensagens[proc].put(Mensagem(
                    	"release", self.lamport_clock, 
                    	self.nome, proc))
                    self.lamport_clock += 1
                self.temRecurso, self.pedido = False, False
                continue
            # solicita recurso
            if not self.pedido:
                # requisição
                print("Processo {} solicitando recurso".format(
                	self.nome))
                self.requisicoes_fila.append(Mensagem(
                	"request", self.lamport_clock, 
                	self.nome, self.nome))

                # Broadcast da requisição feita
                for proc in self.outrosProcessos:
                    fila_mensagens[proc].put(Mensagem(
                    	"request", self.lamport_clock, 
                    	self.nome, proc))
                    self.lamport_clock += 1
                self.pedido = True
            else:
                # Apenas espere até que esteja disponível processando mensagens
                print("Processo {} esperando por mensagem".format(self.nome))
                msg = fila_mensagens[self.nome].get(block=True)  

                # Checagem de rotulo de tempo ao receber uma mensagem, se for maior que o clock, avança
                if msg.rotulo_data >= self.lamport_clock:
                    self.lamport_clock = msg.rotulo_data + 1
                print("Recebeu mensagem: {}".format(msg))
                self.processandoMsg(msg)
                self.lamport_clock += 1

                # Após processar, verifica se o recurso está disponível, se sim, pode usar
                # Também é verificado se recebeu msg antiga de outros, a primeira solicitação precisa ser nossa 
                if self.checkDisponi():
                    print("Recurso disponível para {}".format(self.nome))
                    self.temRecurso = True
            print("Processo {}: {}".format(self.nome, self.requisicoes_fila))
            print("Processo {} Clock: {}".format(self.nome, self.lamport_clock))
            time.sleep(1)

    def checkDisponi(self):
        req_antigo = {k: False for k in self.outrosProcessos}
        # Obtem rotulo de data do pedido
        req_atual = None
        for req in self.requisicoes_fila:
            if req.emissor == self.nome:
                req_atual = req
        if req_atual is None:
            return False
        # Ao pegar o rótulo, verificar se é mais novo do que os outros
        for req in self.requisicoes_fila:
            if req.emissor in req_antigo and req.rotulo_data > req_atual.rotulo_data:
                req_antigo[req.emissor] = True
        if all(req_antigo.values()):
            return True
        return False



t1 = Processo("A", processo_inicial, list(procs - set("A")))
t2 = Processo("B", processo_inicial, list(procs - set("B")))
t3 = Processo("C", processo_inicial, list(procs - set("C")))

#se o processo principal morrer os outros tbm morrem
t1.setDaemon(True)
t2.setDaemon(True)
t3.setDaemon(True)

try:
    t1.start()
    t2.start()
    t3.start()
    while True:
        t1.join(100)
        t2.join(100)
        t3.join(100)
#nunca chega aqui
except KeyboardInterrupt:
    print("Ctrl-c pressed")
    print("Resource usage:")
    print(eventos_counts)
    sys.exit(1)
'''
Hidrometro: 
- se conecta ao broker da Nevoa
- ouve requisicoes de bloqueio/desbloqueio vindas do nó (solicitadas da nuvem pela api)
- publica para o servidor Nevoa
- faz verificações de irregularidades e bloqueia quando necessário
- atualiza sua taxa de consumo
'''

import random
import threading
import time

from datetime import datetime
from hidrometro import Hidrometro
from paho.mqtt import client as mqtt_client

#--------Comandos para teste no cmd ------------------
#mosquitto_sub -t [topico] -h [broker]
#mosquitto_pub -t [topico] -h [broker] -m "[mensagem]"

#Inicia um hidrometro
MATRICULA = random.randint(0,1000) #Adiciona um numero aleatório na matricula
hidrometro =  Hidrometro(MATRICULA, True, True, 3, False, 10)

#Broker para conexão
broker = 'localhost'
port = 1884

#Define o local do hidrometro de maneira aleatória
locais = ['norte','leste','oeste','sul'];
local = locais[0]
topicpub = "hidrometros/" + local + "/consumo/"
topicSub= "hidrometros/" + local + "/status/"

# Criando o id
client_id = f'hidrometro-{MATRICULA}'
username = ''
password = ''

'''Bloco de conexão do hidrometro'''
def connect_mqtt(username, password) -> mqtt_client: 
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print()
        else:
            print("Falha de conexão, código: %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#Subscribe na nevoa para ouvir requisições: -----------------------
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        msgRecebida = str(MATRICULA) #Transforma em str a matricula para comparação
        if msg.payload.decode() == msgRecebida + "/ativo": #Verifica se o que foi recebido é "codigoH/ativo"
            ativaHidro() #Caso verdadeiro, vai para função de verificação para ativação
        elif msg.payload.decode() == msgRecebida + "/bloqueio": #caso seja "codigoH/bloqueio":
            hidrometro.novoStatus(False) #Bloqueia o hidrometro
    client.subscribe(topicSub)
    client.on_message = on_message
    #----------------------------------------------------------------
#Publish para envio de dados ------------------------
def publish(client):
    while True:
        time.sleep(1) #Tempo para não sobrecarregar o envio e ser possivel a leitura
        now = datetime.now() #recebe o horario exato
        data = now.strftime("%d/%m/%Y %H:%M:%S") #transforma em str
        matricula = hidrometro.getMatricula() #recebe a matricula do hidrometro atual
        consumo = hidrometro.getConsumo() #recebe a consumo do hidrometro atual
        status = hidrometro.getStatus() #recebe a status do hidrometro atual

        #Criação do dicionário para o envio de dados
        hidrometroNovo = { 
            'codigoH': matricula,     
            'consumo': consumo,
            'data': data,
            'funcionamento': status
        }

        msg = hidrometroNovo;
        result = client.publish(topicpub, f'{msg}') #tenta fazer o publish
        # resultado da tentativa : [0, 1]
        status = result[0]
        if status == 0: #Caso seja um sucesso:
            print(f"Mandando: `{msg}`, para o topico: `{topicpub}`")
            print()
        else: #Caso contrário:
            print(f"Falha ao mandar mensagem para o topico: {topicpub}")

#Função para atualização de consumo do hidrometro
def atualizaConsumo():
    while True:
        if hidrometro.funcionamento == True: #Caso não esteja bloqueado
            consumo = hidrometro.getConsumo() #Salva em uma variavel o valor do consumo
            vazao = hidrometro.getVazao() #Salva em uma variavel o valor da vazão
            novoValor = consumo + vazao; #Soma consumo + vazão
            hidrometro.setConsumo(novoValor); #Adiciona o novo valor no hidrometro
            time.sleep(2) #Tempo para uma nova atualização

#Fica o tempo todo verificando se existe vazamento:
def  verificaVazamento():
    while True:
        if hidrometro.vazamentos(): #Caso a vazão seja maior que o vazão padrão:
            print("Alerrtaaa vazamento!")
        time.sleep(2)


#Função que bloqueia caso irregularidades
def bloqueioInsta():
    while True:
        vazao = hidrometro.getVazao();
        valorMax = hidrometro.getValorMax()
        contaPaga = hidrometro.getContaPaga()

        if (vazao > valorMax): #verifica caso tenha vazão maior que o valor máximo estabelecido
            hidrometro.novoStatus(False)
        elif (contaPaga == False):  #verifica se a conta do usuario está paga
            hidrometro.novoStatus(False);

#Função para desbloqueio do hidrometro
def ativaHidro():
    funcionamento = hidrometro.getStatus()
    contaPaga= hidrometro.getContaPaga()
    vazao= hidrometro.getVazao()
    valorMax = hidrometro.getValorMax()

    if(funcionamento == False): #Verifica se está bloqueado
        if (contaPaga == True): #Caso esteja, verifica se a conta está paga
            if (vazao < valorMax): #Caso esteja, verifica se a vazão é menor que o valor máximo estabelecido
                hidrometro.novoStatus(True) #Caso todas sejam verdadeiras, ativa o hidrometro

def run():
    #Conexão com o client Mqtt
    client = connect_mqtt(username, password)

    #Threads
    thread1 = threading.Thread(target=atualizaConsumo)   #Thread para atualização de consumo
    thread2 = threading.Thread(target=verificaVazamento) #Thread para verificação de vazamento
    thread3 = threading.Thread(target=publish, args= (client,)) #Thread para publicação no broker
    thread4 = threading.Thread(target=bloqueioInsta) #Thread para verificação de irregularidades

    #Iniciando as threads
    thread1.start()                               
    thread2.start()                               
    thread3.start()                              
    thread4.start() 

    #Se inscrevendo no topico de bloqueio/desbloqueio
    subscribe(client)
    client.loop_forever()
    
run()

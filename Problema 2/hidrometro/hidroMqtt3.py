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
local = locais[3]
topicpub = "hidrometros/" + local + "/consumo/"
topicSub= "hidrometros/" + local + "/status/"

# Criando o id
client_id = f'hidrometro-{MATRICULA}'
username = ''
password = ''


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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        msgRecebida = str(MATRICULA)
        if msg.payload.decode() == msgRecebida + "/ativo":
            ativaHidro()
        elif msg.payload.decode() == msgRecebida + "/bloqueio":
            hidrometro.novoStatus(False)
    client.subscribe(topicSub)
    client.on_message = on_message

def publish(client):
    while True:
        time.sleep(1)
        now = datetime.now()
        data = now.strftime("%d/%m/%Y %H:%M:%S")
        matricula = hidrometro.getMatricula()
        consumo = hidrometro.getConsumo()
        status = hidrometro.getStatus()

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
        if status == 0:
            print(f"Mandando: `{msg}`, para o topico: `{topicpub}`")
            print()
        else:
            print(f"Falha ao mandar mensagem para o topico: {topicpub}")

def atualizaConsumo():
    while True:
        if hidrometro.funcionamento == True:
            consumo = hidrometro.getConsumo() #Salva em uma variavel o valor
            vazao = hidrometro.getVazao() #Salva em uma variavel o valor
            novoValor = consumo + vazao; #Soma consumo + vazão
            hidrometro.setConsumo(novoValor); #Adiciona o novo valor no hidrometro
            time.sleep(2)

#Fica o tempo todo verificando se existe vazamento:
def  verificaVazamento():
    while True:
        if hidrometro.vazamentos():
            print("Alerrtaaa vazamento!")
        time.sleep(2)


#Função que bloqueia caso irregularidades
def bloqueioInsta():
    while True:
        vazao = hidrometro.getVazao();
        valorMax = hidrometro.getValorMax()
        contaPaga = hidrometro.getContaPaga()

        if (vazao > valorMax):
            hidrometro.novoStatus(False)
        elif (contaPaga == False): 
            hidrometro.novoStatus(False);

#Função para desbloqueio do hidrometro
def ativaHidro():
    funcionamento = hidrometro.getStatus()
    contaPaga= hidrometro.getContaPaga()
    vazao= hidrometro.getVazao()
    valorMax = hidrometro.getValorMax()

    if(funcionamento == False):
        if (contaPaga == True):
            if (vazao < valorMax):
                hidrometro.novoStatus(True)

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

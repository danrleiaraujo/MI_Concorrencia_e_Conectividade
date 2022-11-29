import socket
import random
import sys
import ast

from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt

'''
Conecta ao broker e diz que está online
~ Pelo oq estou entendendo:
-> Tenho que conectar ao broker, avisar que estou online, depois receber uma lista de lojas online e salvar.
-> Caso a lista seja igual ao que já tem, não salva
'''

#--------Comandos para teste no cmd ------------------
# cd C:\Program Files\mosquitto
# mosquitto_sub -t [topico] -h [broker]
# mosquitto_sub -t "/lojas/online/" -h "localhost"

# mosquitto_pub -t [topico] -h [broker] -m "[mensagem]"
# mosquitto_pub -t "/lojas/online/" -h "localhost" -m "online"

#Broker para conexão    
broker = 'localhost'
port = 1883
topicSub = "/lojas/online/"
keep_alive_broker = 60 
MATRICULA = random.randint(0,1000) #Adiciona um numero aleatório na matricula

# Criando o id
client_id = socket.gethostbyname(socket.gethostname()) #Salva o IPLocal como cliente_id

# Caso o broker tenha usuario e senha: (Não é o nosso caso)
username = '' 
password = ''

#Lojas online
lojasOnline = {
    MATRICULA: client_id 
}

'''Bloco de conexão'''
def on_connect(client, userdata, flags, rc):
    print("[STATUS] Conectado ao Broker.")
    #faz subscribe automatico no topico
    lojas = str(lojasOnline)
    client.publish(topicSub, lojas)
    client.subscribe(topicSub)

#Callback - mensagem recebida do broker
#toda vez que uma mensagem for recebida do broker, esta funcao sera chamada
def on_message(client, userdata, msg):
    global lojasOnline
    
    lojas = str(lojasOnline)

    MensagemRecebida = ast.literal_eval(msg.payload.decode())    

    if(len(lojasOnline) > len(MensagemRecebida)):
        client.publish(topicSub, lojas)
    else:   
        for nome in MensagemRecebida:
            lojasOnline[nome] = MensagemRecebida[nome]
    print(MATRICULA,lojasOnline)
    print()
    
def connect_mqtt(username, password) -> mqtt_client: 
    def on_connect(client, userdata, flags, rc):
        client.subscribe(topicSub)
        if rc != 0:
            print("Falha de conexão, código: %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#---------------------------------------------------------------------------
#Função para rodar:
def run():
    try:
        print("[STATUS] Inicializando MQTT...")
        #inicializa MQTT:
        
        #cria client MQTT e define funcoes de callback de conexao (client.on_connect) 
        #e recepcao de dados recebidos (client.on_message)
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        #faz a conexao ao broker MQTT 
        client.connect(broker, port, keep_alive_broker)

        client.loop_forever()
    except KeyboardInterrupt:
        print ("\nCtrl+C pressionado, encerrando aplicacao e saindo...")
        sys.exit(0)

run()
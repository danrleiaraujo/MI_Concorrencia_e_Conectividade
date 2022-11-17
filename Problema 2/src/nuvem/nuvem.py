import json
import random
import time
from paho.mqtt import client as mqtt_client

'''o banco de dados segue o padrão:
nevoaDB = {
    idNevoa: {
        'media': int - média do nó,
        'hidrometros': [int - codigos dos hidrometros],
        'maiores': [{maiores}, {consumos}, {da nevoa}]
        }
}
'''
# banco de dados com os dados das nevoas
nevoaDB = {}

# conexão mqtt com todas as nevoas
nevoas = {
    'broker': 'localhost',      
    'port': 1883,
    'topicPub': "nuvem",     
    'topicSub': "nuvem/#"
}

#       funções de conectividade com a névoa --------------------------------------
def connect_mqtt(broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(f'{random.randint(0, 100)}')
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    
    return client

clientNevoa = connect_mqtt(nevoas['broker'], nevoas['port'])

def subscribe (client, topico):
    def on_message(client, userdata, msg):
        topico = msg.topic.split('/')
        match (topico[1]):
            case 'media':
                salvarNo(msg)
            case 'consumo':
                if (topico[-1] not in nevoaDB.keys()):
                    pass
                else:
                    # lista com os maiores hidrometros daquela nevoa
                    nevoaData = json.loads(msg.payload.decode())
                    nevoaDB[topico[-1]] = nevoaData    #   uma lista com os maiores consumos
            case _:
                pass

        print(f'{msg.payload.decode()}')
    
    client.subscribe(topico)
    client.on_message = on_message

def publish(client, topic, msg):
    client.publish(topic, msg)

def salvarNo(msg):
    codigoNo = msg.topic.split('/')[-1]
    nevoaDB[codigoNo] = {}
    # a mensagem contendo media e lista de codigos de hidrometros ou maiores hidrometros vira um dicionario
    dicionario = json.loads(msg.payload.decode())
    for key, value in dicionario.items():
        nevoaDB[codigoNo][key] = value

def subMaioresConsumos (client):
    def on_message(client, userdata, msg):
        print(f'{msg.payload.decode()}')
        idNevoa = msg.topic.split('/')[-1]
        nevoaData = json.loads(msg.payload.decode())
        nevoaDB[idNevoa] = nevoaData    #   uma lista com os maiores consumos
    
    client.subscribe(f'{nevoas["topicPub"]}/consumo/#')
    client.on_message = on_message

#   -------------------------------------------------------------------------

#       funções de requisicoes para a névoa ---------------------------------
def maiorConsumo(param):
    global clientNevoa
    # A nuvem irá enviar uma mensagem para o topico nuvem/consumo
    # contendo o valor n=param referente a quantidade max de hidrometros 
    # na lista de maiores consumidores que ela quer ver.
    publish(clientNevoa,f'{nevoas["topicPub"]}/consumo', f'{param}')
    time.sleep(5)
    # como resposta a nevoa retorna a lista em json dos maiores hidrometros.
    # da nuvem central a lista deve ir para uma pagina web

def tempoReal(param):
    print()
    # TODO
    # Enviar uma mensagem (conteúdo: param) para o topico nuvem/temporeal/nevoaquecontemohidrometro
    # onde Param será o id do hidrometro que ele selecionou para ver.
    # a nevoa irá publicar em tempo real nesse topico (nuvem/status/idHidro) da nuvem
    # a nuvem deve se inscrever e mandar os dados para a pagina web via websocket.

#   -----------------------------------------------------------------------------

def run ():
    global clientNevoa
    subscribe(clientNevoa, nevoas['topicSub'])
    clientNevoa.loop_forever()


run()
    
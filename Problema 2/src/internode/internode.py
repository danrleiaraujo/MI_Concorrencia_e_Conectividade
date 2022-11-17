'''
A névoa: 
- se conecta ao broker da nuvem (central)
- ouve requisicoes da nuvem (solicitadas a nuvem pela api)
- ouve atualização de status dos hidrometros (que sao enviadas ao topico da nevoa)
- publica para o servidor central as infos dos hidrometros
- publica para os hidrometros a mensagem de bloqueio quando necessário
'''
import time
import ast
import threading

from paho.mqtt import client as mqtt_client

# infos dos hidrometros -------------------------------------
'''
Hidrômetros neste nó (db)
Cada hidrômetro será uma entry no dicionário seguindo:
{
    codigoH: int, 
    consumo: int (em m3),
    data: datatime (timestamp),
    funcionamento: boolean
}
'''
hidroDB= {}

#   brokers ---------------------------------------------------------------
central = {
    'broker': 'localhost',      # mudar para maquina central do larsid
    'port': 1883,
    'topicPub': "nuvem",     # como gerar id para cada no criado?
    'topicSub': "nuvem/#"
}

locais = ['norte','leste','oeste','sul'];
local = locais[2]
topicpub = 'hidrometros/' + local + '/status/'
topicsub= 'hidrometros/' + local + '/consumo/'
username = "" 
password = ""

hidrometros = {
    'broker': 'localhost',  # mudar para maquina hidrometros do larsid
    'port': 1884,
    'topicPub': topicpub,
    'topicSub': topicsub
}

# valores globais ------------------------------------------------------------
LIMITE_CONSUMO = 50
MEDIA_NEVOA = 0

#       funcões de operações no banco de dados -------------------------------
# Salva um novo status do hidrometro no DB
# cliente é a instacia mqtt criada na conexão com o broker que se quer ouvir
def salvarHidrometro(msg):     # o nó ouve do hidrometro
    hidroData = msg.payload.decode()    # converte a mensagem do hidrômetro em um dicionário
    dictionary = ast.literal_eval(hidroData)
    print(dictionary)
    
    codigoH = dictionary['codigoH']
    if (codigoH in hidroDB.keys()):
        hidroDB[codigoH].insert(0, dictionary)
    else:
        hidroDB[codigoH] = [dictionary]
    return codigoH

def ultimoRegistro(hidroDB):
    ultimoRegistro = []
    # iterar sobre todas as chaves de hidroDB (todos os hidrometros)
    for k in hidroDB.keys():
    # pegar o registro mais recente (indice 0) de cada um deles -- cada registro é um dicionario
        ultimoRegistro.append(hidroDB[k][0])
    
    return ultimoRegistro   # lista de dicionarios


#       funções de conectividade com a nuvem e hidrometros ----------------------------
# publica automaticamente sua media parcial para a nuvem 
# (client: cliente da nuvem)
def pubMedia(client):
    while True:
        total = 0
        if (len(hidroDB.items())!=0):
            for k in hidroDB:
                total += hidroDB.get(k)[0].get('consumo')
            print ("total:", total)
            mediaNevoa = total // len(hidroDB.keys())
            print ("media nevoa:", mediaNevoa)

            global MEDIA_NEVOA
            MEDIA_NEVOA = mediaNevoa

            hidrolist = hidroDB.keys()
            msg = {
                'media': mediaNevoa,
                'hidrometros': hidrolist
            }
            # topico media : nuvem/media/:idnevoa
            print('Enviando media')
            client.publish(f'{central["topicPub"]}/media/{client._client_id.decode()}', f'{msg}')
            time.sleep(5)

#Realiza o publish no topico
def publish(client, topic, msg):
    client.publish(topic, msg)
    
#Conexão de subscribe mqtt-----------------------------------------
def connect_mqtt(username, password, broker, port) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker! Na porta:")
            print(port)
        else:
            print("Failed to connect, return code %d\n", rc)

    client_id = f'internode_18211205'
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client, topicsub):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic == topicsub:
            codigoH = salvarHidrometro(msg)
            global LIMITE_CONSUMO
            consumoAtual = hidroDB[codigoH][0]['consumo']
            
            if ((consumoAtual > LIMITE_CONSUMO) or
                (consumoAtual > MEDIA_NEVOA)):   # checa consumo + recente
                msg = str(codigoH) + "/bloqueio"
                publish(client, f'{hidrometros["topicPub"]}', f'{msg}')

            elif((consumoAtual <= LIMITE_CONSUMO) and
                (consumoAtual <= MEDIA_NEVOA)):
                msg = str(codigoH) + "/ativo"
                publish(client, f'{hidrometros["topicPub"]}', f'{msg}')



    client.subscribe(topicsub)
    client.on_message = on_message
#-------------------------------------------------------------------------
#Realizando Subscribes na nuvem e hidrometros:
def subscribers():
    while True:
        clientHidro = connect_mqtt(username, password, hidrometros['broker'], hidrometros['port'])
        clientHidro.loop_start()
        subscribe(clientHidro, hidrometros['topicSub'])
        time.sleep(0.5)
        clientHidro.loop_stop()
        clientHidro.disconnect()

        clientCentral= connect_mqtt(username, password, central['broker'], central['port'])
        clientCentral.loop_start()
        subscribe(clientCentral, central['topicSub'])
        time.sleep(0.5)
        clientCentral.loop_stop()
        clientCentral.disconnect()

#   -----------------------------------------------------------------------------

def run():
    clientCentral= connect_mqtt(username, password, central['broker'], central['port'])
    #   Threads
    thread1 = threading.Thread(target=subscribers)   #Thread para subscrever no topico = 'hidrometros/' + local + '/consumo/' 
    thread2 = threading.Thread(target=pubMedia, args=(clientCentral,))
    
    #   Iniciando as threads
    thread1.start()  
    thread2.start()    

run()
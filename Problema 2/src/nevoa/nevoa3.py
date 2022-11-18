'''
A névoa: 
- se conecta ao broker da nuvem
- ouve requisicoes da nuvem (solicitadas a nuvem pela api)
- ouve atualização de status dos hidrometros 
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
    data: datatime (datetime.now),
    funcionamento: boolean
}
'''
#Variaveis globais
hidroDB= {}
locais = ['norte','leste','oeste','sul'];
local = locais[3]
client_id = f'hidrometro-{local}'
no_id = local
topicpub = 'hidrometros/' + local + '/status/'
topicsub= 'hidrometros/' + local + '/consumo/'
username = "" 
password = ""

#   brokers ---------------------------------------------------------------
central = {
    'broker': 'localhost',      
    'port': 1883,
    'topicPub': "nuvem",    
    'topicSub': "nuvem/#"
}
hidrometros = {
    'broker': 'localhost',  
    'port': 1884,
    'topicPub': topicpub,
    'topicSub': topicsub
}

# Constantes globais ------------------------------------------------------------
LIMITE_CONSUMO = 50
MEDIA_NEVOA = 0

#       funcões de operações no banco de dados -------------------------------
# Salva um novo status do hidrometro no DB
# cliente é a instacia mqtt criada na conexão com o broker que se quer ouvir
def salvarHidrometro(msg):     # o nó ouve do hidrometro
    hidroData = msg.payload.decode()    #recebe a mensagem para conversão
    dictionary = ast.literal_eval(hidroData) # converte a mensagem do hidrômetro em um dicionário

    codigoH = dictionary['codigoH'] #Salva o código do hidrometro

    if (codigoH in hidroDB.keys()): #se já existir no banco de dados:
        hidroDB[codigoH].insert(0, dictionary) #altera o valor que já existe
    else:
        hidroDB[codigoH] = [dictionary] #Caso não exista, adiciona no banco
    return codigoH #retorna o código do hidrometro

def ultimoRegistro(hidroDB):
    ultimoRegistro = []
    for k in hidroDB.keys(): # iterar sobre todas as chaves de hidroDB (todos os hidrometros)
    # pegar o registro mais recente (indice 0) de cada um deles -- cada registro é um dicionario
        ultimoRegistro.append(hidroDB[k][0])

    return ultimoRegistro   # lista de dicionarios


#       funções de conectividade com a nuvem e hidrometros ----------------------------
# publica automaticamente sua media parcial para a nuvem 
def pubMedia():
    while True:
        total = 0
        if (len(hidroDB.items())!=0): #Se o banco não estiver vazio:
            for k in hidroDB:
                total += hidroDB.get(k)[0].get('consumo') #soma os consumos até então
            mediaNevoa = total // len(hidroDB.keys()) #realiza a média sendo o total dos consumos dividido pela quantidade de hidro

            global MEDIA_NEVOA
            MEDIA_NEVOA = mediaNevoa #atualiza a variavel global

            hidrolist = hidroDB.keys() #salva os hidrometros em lista

            msg = { #cria um dicionario para o envio para nuvem
                'media': mediaNevoa,
                'hidrometros': hidrolist
            }
            topico = f'{central.get("topicPub")}/media/{no_id}' #cria um tópico (nuvem/media/nevoa)
            print('Enviando media')
            publish(clientCentral, topico, f'{msg}')
            time.sleep(5)

#Realiza o publish no topico
def publish(client, topic, msg): #recebe o client conectado ao broker, o topico para o envio e a mensagem
    client.publish(topic, msg)
    
#Conexão de subscribe mqtt-----------------------------------------
def connect_mqtt(username, password, broker, port) -> mqtt_client: #recebe o usuario, senha, broke e a porta de conexão
    def on_connect(client, userdata, flags, rc):
        if rc == 0: #Retorna 0 caso a conexão seja um sucesso
            print()
        else: 
            print("Failed to connect, return code %d\n", rc)

    client_id = f'internode_18211205' #id da nevoa para subscribe
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client, topicsub): #Recebe o cliente conectado no broker e o topico
    def on_message(client, userdata, msg):
        print(f"Recebido: `{msg.payload.decode()}` de `{msg.topic}`")
        if msg.topic == topicsub: #Se for do tópico do hidrometro:
            codigoH = salvarHidrometro(msg) #Salva o hidrometro no banco de dados
            global LIMITE_CONSUMO 
            consumoAtual = hidroDB[codigoH][0]['consumo']
            
            if ((consumoAtual > LIMITE_CONSUMO) or
                (consumoAtual > MEDIA_NEVOA)):   # checa consumo + recente - > Caso verdadeiro, bloqueia o hidro
                msg = str(codigoH) + "/bloqueio" #A mensagem vira: CodigoDoHidrometro/bloqueio
                publish(client, f'{hidrometros["topicPub"]}', f'{msg}') 

            elif((consumoAtual <= LIMITE_CONSUMO) and
                (consumoAtual <= MEDIA_NEVOA)): #-> Caso verdadeiro, desbloqueia/ativa o hidro
                msg = str(codigoH) + "/ativo" #A mensagem vira: CodigoDoHidrometro/ativo
                publish(client, f'{hidrometros["topicPub"]}', f'{msg}')
        else: #Caso não seja o hidrometro, poderá ser a núvem, sendo assim:
            if(msg.topic == "nuvem/consumo"):  #verifica se é o tópico de nuvem/consumo
                # A nuvem irá enviar uma mensagem para o topico nuvem/consumo
                # contendo o valor n referente a quantidade max de hidrometros 
                # na lista de maiores consumidores.
                s = msg.payload.decode('utf-8')
                try:
                    top_n = int(s)
                except:
                    top_n = (len(hidroDB.keys())*0.3)
                
                lista = ultimoRegistro(hidroDB)
                # ordenar todos os items
                ordenada = sorted(lista, key=lambda d: d['consumo'], reverse=True)
                #pegar n maiores
                maiores = [it for it in ordenada if ordenada.index(it) < top_n]

                msg = {
                    'maiores': maiores
                }
                # nuvem/consumo/idNevoa : { maiores = [] }
                client.publish(f'{central["topicPub"]}/consumo/{client_id}', msg )

            elif(msg.topic == "nuvem/limiteconsumo"): #verifica se é o tópico de nuvem/limiteconsumo para um novo limite de consumo
                try:
                    LIMITE_CONSUMO = int(msg.payload.decode())
                    print('Limite de consumo atualizado!')
                except:
                    pass
        
    client.subscribe(topicsub)
    client.on_message = on_message
#-------------------------------------------------------------------------
#Realizando Subscribes na nuvem e hidrometros:
def subscribers():
    while True:
        clientHidro = connect_mqtt(username, password, hidrometros['broker'], hidrometros['port']) #Conecta no broker na porta do hidro
        clientHidro.loop_start() #Inicia o loop de conexão
        subscribe(clientHidro, hidrometros['topicSub']) #Realiza o subscribe
        time.sleep(0.5) #tempo para recebimento de mensagens
        clientHidro.loop_stop() #para o loop
        clientHidro.disconnect() #desconecta o client para o inicio do proximo

        clientCentral= connect_mqtt(username, password, central['broker'], central['port']) #Conecta no broker na porta da nuvem
        clientCentral.loop_start() #Inicia o loop de conexão
        subscribe(clientCentral, central['topicSub'])#Realiza o subscribe
        time.sleep(0.5) #tempo para recebimento de mensagens
        clientCentral.loop_stop() #para o loop
        clientCentral.disconnect() #desconecta o client para o inicio do proximo

#   -----------------------------------------------------------------------------

clientCentral= connect_mqtt(username, password, central['broker'], central['port'])

def run():
    #   Threads
    thread1 = threading.Thread(target=subscribers)   #Thread para subscrever no topico = 'hidrometros/' + local + '/consumo/' 
    thread2 = threading.Thread(target=pubMedia) #Thread para o publisher da média dos hidrometros alocados no banco de dicionário
    
    #   Iniciando as threads
    thread1.start()  
    thread2.start()    

run()
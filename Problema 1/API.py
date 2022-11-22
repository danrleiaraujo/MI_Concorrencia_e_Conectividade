#importações
import socket
import threading
import time
import http.server

#Constantes:
FORMATO = 'utf-8' 
SERVER = "127.0.0.1"
PROTOCOL= "HTTP/1.0"
#--------------------------------------------------------------------------------
#função que bloqueia ou desbloqueia hidrometro através de comunicação TCP
def funcionamento():
    #TCP - Funcionamento do hidrometro
    PORT = 8080 #Porta
    ADDR_S= (SERVER, PORT) #Endereço  
    while True:
        try:   
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #inicia uma variavel como tcp
            tcp.connect(ADDR_S) #conecta no servidor
            try:
                n= 0;
                while (n != 1):
                    escolha = input("Digite 1-> para Bloqueio/Desbloqueio do hidrometro\n Digite 2->Aumento de Vazão\n")
                    if(escolha == '1'):
                        mensagem = input('Digite se deseja Ativar ou Desativar o hidrômetro: ')
                        enviar = ("Hidrometro="+ mensagem)
                        n=1
                    elif(escolha == '2'):
                        mensagem = input('Digite a nova vazao do hidrômetro: ')
                        enviar = ("Vazao="+ mensagem)
                        n=1
                    else:
                        print("Opção Inválida")
                tcp.send(enviar.encode(FORMATO)) #Comando para enviar dados
                time.sleep(10)                                         #pausa para envio de dados
                respostaSistema = tcp.recv(1024) #Resposta do sistema se foi recebido 
                respostaSistema = respostaSistema.decode(FORMATO) #como vem em formato de byte, precisa de um decode
                print("Recebido do servidor: ",respostaSistema)
            finally:
                print('Fechando conexão...')
                tcp.close() #Fecha a conexão
        except:
            print("Servidor TCP desligado, tente novamente mais tarde.")
            time.sleep(10) #Tempo para uma nova tentativa
#--------------------------------------------------------------------------------  
#função que recebe informações do hidrometro
def recebeDados():
    #UDP - Servidor para recebimento de dados
    PORT = 8090
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Inicia uma variavel com socket udp
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    orig = (SERVER, PORT) #Endereço
    udp.bind(orig) #Começa a ouvir
    print("Ligado o Servidor UDP")
    try:
        while True:
            msg, cliente = udp.recvfrom(1024) #Recebe em bites a mensagem e o client
            print ("Cliente: ", cliente) #Recebe em bites, então necessário uma conversão
            print ("Consumo: ", msg.decode(FORMATO)) #Recebe em bites, então necessário uma conversão
            time.sleep(6) #pausa para receber dados
            if not msg: break
            
    finally:
        
        print ("Fechada a conexão com: ", cliente) 
        udp.close() #Fecha a conexão udp
#--------------------------------------------------------------------------------
 
#função que inicia um servidor http no LocalHost
def servidor():
    SERVERCLASS  = http.server.HTTPServer 
    HANDLERCLASS = http.server.SimpleHTTPRequestHandler 
    situacoes = http.server.BaseHTTPRequestHandler
    port = 8000
    server_address = ('127.0.0.1', port) 
    HANDLERCLASS.protocol_version = PROTOCOL 
    http_server = SERVERCLASS(server_address, HANDLERCLASS) 
    sa = server_address
    print("Servidor on: ", sa[0], "porta", sa[1], "...") 
    http_server.serve_forever()
#--------------------------------------------------------------------------------
def iniciar():
    #Bloqueio e desbloqueio de hidrometro
    thread1 = threading.Thread(target=funcionamento)
    
    #Recebe dados do hidrometro
    thread2 = threading.Thread(target=recebeDados)

    #Servidor HTTP
    thread3 = threading.Thread(target=servidor)

    thread1.start()
    time.sleep(0.5)                                         #pausa para envio de dados

    thread2.start()
    time.sleep(0.5)                                         #pausa para envio de dados

    thread3.start()   
#--------------------------------------------------------------------------------------
iniciar()
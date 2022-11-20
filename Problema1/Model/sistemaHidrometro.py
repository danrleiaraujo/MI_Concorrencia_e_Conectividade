from hidrometro import Hidrometro #importa Hidrometro para transforma-lo em um client socket

#Importação de bibliotecas
import socket
import threading
import time
import random

#Criação de constante de localhost como ip de servidor
SERVER = "127.0.0.1"

#Criação de constante de porta para situação client e situação serve
PORT_CLIENT = 8090 #Porta
PORT_SERVER = 8080

#Constante para formato utf-8
FORMATO = 'utf-8' 
MATRICULA = random.random() #Adiciona um numero aleatório na matricula
#Inicia um hidrometro
hidrometro =  Hidrometro(MATRICULA, "Av. José Botelho, 123", True, 3, 5, False)
#--------------------------------------------------------------------------------
#função que envia os dados do hidrometro
def enviaDados():
    #UDP - Envio de dados
    ADDR_C = (SERVER, PORT_CLIENT)    #Endereço
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     #configuração UDP
    while True:
        if(hidrometro.getStatus() == True): #Verifica se o hidrometro não está bloqueado
            #Envio
            msg = str(hidrometro.getConsumo())                               #converte para string o consumo
            while msg != '\x18':
                udp.sendto(msg.encode('utf-8'),ADDR_C)                  #Codificação da mensagem 
                time.sleep(6)                                         #pausa para envio de dados
                msg = str(hidrometro.getConsumo())                      #Atualiza o consumo
                if (hidrometro.getStatus() == False):                   #Faz uma nova verificação se não está bloqueado
                    print("Seu hidrômetro foi bloqueado!");
                    break
                if not msg: break
            udp.close()
        else:
            print("Seu hidrômetro encontra-se bloqueado. Matricula: ", hidrometro.getMatricula()) #Manda aviso que está bloqueado com a matricula
            time.sleep(6) #Tempo para uma nova verificação    
#--------------------------------------------------------------------------------  
 
#função que recebe o bloqueio e desbloqueio do hidrometro  - em 'funcionamento" 
def recebeDados():
    #TCP - Recebimento de dados
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #conexão TCP
    ADDR_S = (SERVER, PORT_SERVER) #Endereço  
    tcp.bind(ADDR_S) #Configura o endereço
    tcp.listen(10) #Começa a ouvir até 10 conexões
    
    while(True):
        print("Esperando por conexões:")
        con, cliente = tcp.accept() #Aceita conexão
        print("Conctado por: ", cliente)
        try:
            while True:			
                msg = con.recv(1024).decode(FORMATO) #Começa a receber mensagens em byte, por isso a conversão para o formato utf-8
                try:
                    mensagem_separada = msg.split("=") #Divide a mensagem no '=' (Pré estabelecido no outro arquivo)
                    funcionamento = mensagem_separada[1] #Recebe o funcionamento
                    print("Mensagem: ",msg)
                    tcp.sendall(b'Recebido!') #Manda uma mensagem de recebido para o client
                except:
                    print("")
                finally:
                    if not msg: break #Caso não tenha mais mensagem, dá um break no while de recebimento de mensagens
        

                if(msg.startswith("Hidrometro=")): #Se a mensagem começar com hidrometro:
                    if(funcionamento == "ligado" or funcionamento == "Ligado" or funcionamento == "funcionando" or funcionamento == "Funcionando"or funcionamento == "ativar" or funcionamento == "Ativar" or funcionamento == "ligar" or funcionamento == "Ligar"):
                        hidrometro.novoStatus(True) #O estado do hidrometro fica "Ligado"

                    elif(funcionamento == "desligado" or funcionamento == "Desligado" or funcionamento == "desativado" or funcionamento == "Desativado" or funcionamento == "desativar" or funcionamento == "Desativar"):
                        hidrometro.novoStatus(False) #O estado do hidrometro fica "desligado"
                        
                    else:
                        print("Talvez tenha escrito errado, por favor tente novamente");
                elif(msg.startswith("Vazao=")): #Caso inicie com 'Vazao='
                    vazao=int(funcionamento) #Converte o dado para int
                    hidrometro.setVazao(vazao) #Coloca o novo valor no hidrometro.do
        except:
            print("Sem conexão")
        finally:	
            print ('Finalizando conexao do cliente',cliente)            #finaliza a conexão com o cliente
            print("O hidrômetro encontra-se no estado atual de: ",hidrometro.getStatus())


#--------------------------------------------------------------------------------
def atualizaConsumo(): #Função para atualização do consumo
    while True:
        if hidrometro.getStatus() == True: #Verifica se o hidrometro está bloquea
            print("Consumo:", hidrometro.getConsumo()) #Mostra o consumo atual
            print("Vazao:", hidrometro.getVazao()) #Mostra a vazão atual
            consumo = hidrometro.getConsumo() #Salva em uma variavel o valor
            vazao = hidrometro.getVazao() #Salva em uma variavel o valor
            novoValor = consumo + vazao; #Soma consumo + vazão
            hidrometro.setConsumo(novoValor); #Adiciona o novo valor no hidrometro
            time.sleep(6) #Tempo para uma nova atualização - 6s o mesmo valor que o tempo de espera para envio de mensagens

#--------------------------------------------------------------------------------
def verificaVazamento(): #Função para verificação de vazamento  
    while True:
        if (hidrometro.vazamentos() == True):   #Caso tenha vazamento:
            print("Alerta de vazamento! No hidrometro: ", hidrometro.getMatricula()) #Manda um alerta
        else: #Caso contrário:
            print("Sem vazamentos"); #Sem vazamento
        time.sleep(15) #Tempo de espera para uma nova verificação
#--------------------------------------------------------------------------------
def iniciar():
    
    thread1 = threading.Thread(target=enviaDados)        #Thread para envio de dados UDP
    thread2 = threading.Thread(target=recebeDados)       #Thread para recebimento de solicitação em TCP
    thread3 = threading.Thread(target=atualizaConsumo)   #Thread para atualização de consumo
    thread4 = threading.Thread(target=verificaVazamento) #Thread para verificação de vazamento

    thread1.start()                               
    thread2.start()                             
    thread3.start()      
    thread4.start()      
#--------------------------------------------------------------------------------------
iniciar()
import socket
import threading

ServerIP = '127.0.0.1'
PORT = 6665

#Conexão com o servidor
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    username = input('Nome de usuário: ')
    client.connect((ServerIP,PORT))
    print(f'Conexão realizada em {ServerIP}:{PORT}')
except:
    print(f'ERROR: A conexão não pode ser realizada em: {ServerIP}:{PORT}')

#recebimento de mensagens
def receiveMessage():
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message=='getUser':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            print('ERROR: Servidor indisponível')

#envio de mensagem
def sendMessage():
    while True:
        client.send(input().encode('utf-8'))
        
#divisão das tarefas
thread1 = threading.Thread(target=receiveMessage,args=()) 
thread2 = threading.Thread(target=sendMessage,args=())

thread1.start()
thread2.start()
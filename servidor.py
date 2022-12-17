import socket
import threading

HOST = '127.0.0.1'
PORT = 6665

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print(f'Server está rodando ........... {HOST}:{PORT}')

clients = []
usernames = []

# gera mensagem por cliente
def globalMessage(message):
    for client in clients:
        client.send(message)

#recebe a mensagem e coloca como global
def handleMessages(client):
    while True:
        try:
            receiveMessageFromClient = client.recv(2048).decode('utf-8')
            globalMessage(f'{usernames[clients.index(client)]} :{receiveMessageFromClient}'.encode('utf-8'))
        #Cliente saiu:
        except:
            clientLeaved = clients.index(client)
            client.close()
            clients.remove(clients[clientLeaved])
            clientLeavedUsername = usernames[clientLeaved]
            globalMessage(f'{clientLeavedUsername} Saiu do servidor'.encode('utf-8'))
            usernames.remove(clientLeavedUsername)

#conexão iinicial do cliente no servidor
def initialConnection():
    while True:
        try:
            client, address = server.accept()
            clients.append(client)
            client.send('getUser'.encode('utf-8'))
            username = client.recv(2048).decode('utf-8')
            usernames.append(username)
            globalMessage(f'{username} Entrou no servidor!'.encode('utf-8'))
            user_thread = threading.Thread(target=handleMessages,args=(client,))
            user_thread.start()
        except:
            pass

#inicia a conexão
initialConnection()
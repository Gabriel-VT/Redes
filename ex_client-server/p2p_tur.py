import os
import socket
import sys
from threading import Thread
import time

HEADER_LENGTH = 5

def GetUdpChatMessage():
    global name
    global broadcastSocket
    global current_online
    while True:
        recved = broadcastSocket.recv(1024).decode('utf-8')

        if not len(recved):
             return False
        username_length = int(recved[:HEADER_LENGTH].strip())
        username = recved[HEADER_LENGTH:HEADER_LENGTH+username_length]
                   
        if username[:1] == 'm':
           
           message_header =recved[HEADER_LENGTH+username_length:HEADER_LENGTH+username_length+HEADER_LENGTH]
           if not len(message_header):
             return False
           message_length = int(message_header.strip())
           message = recved[HEADER_LENGTH+username_length+HEADER_LENGTH:HEADER_LENGTH+username_length+HEADER_LENGTH+message_length]

           print( username[1:] + ">>" + message)

        elif username[:1] == 'o':
          
           if not(username[1:] in current_online):
             current_online.append(username[1:])
             print("***New user: " + username[1:] + "***")
             print('***Total Online User: ' + str(len(current_online))+"***")
             
        elif username[:1] == 's':
           if (user[1:] in current_online):
             current_online.remove(username[1:])
             print("***User disconnected: " + username[1:] + "***")
             print('***Total Online User: ' + str(len(current_online))+"***")

def SendBroadcastMessageForChat():
    global name
    global sendSocket
    sendSocket.setblocking(False)           
    while True:
        data = input(name + ">>")

        if data == 'Exit()':
            username =  ('s'+name).encode('utf-8')
            username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
            sendSocket.sendto(username_header+username, ('255.255.255.255', 2000)) 
            os._exit(1)
            
        elif data != '':
            username =  ('m'+name).encode('utf-8')
            username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
            message = data.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            sendSocket.sendto(username_header+username+message_header+message,('255.255.255.255', 2000))

def SendBroadcastOnlineStatus():
    global name
    global sendSocket
    sendSocket.setblocking(False)
    username =  ('o'+name).encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    while True:                             
        time.sleep(1)

        sendSocket.sendto(username_header+username, ('255.255.255.255', 2000))  


def main():
    global broadcastSocket

    broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   
    broadcastSocket.bind(('0.0.0.0', 2000))                                 
    global sendSocket
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)           
    sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)         

    # Mensagem de inicialização
    print('*************************************************')
    print('*            Welcome to P2P Chatroom            *')
    print('*              To exit type: Exit()             *')
    print('*************************************************')

    #Escolhendo o nome de usuário
    global name
    name = ''                                                   
    while True:                                                 
        if not name:
            name = input('Username: ')
            if not name:
                print('Enter a valid username')
            else:
                break
    print('*************************************************')  

    global recvThread
    recvThread = Thread(target=GetUdpChatMessage)               
    global sendMsgThread
    sendMsgThread = Thread(target=SendBroadcastMessageForChat)  
    global current_online
    current_online = []                                         
    global sendOnlineThread
    sendOnlineThread = Thread(target=SendBroadcastOnlineStatus) 
    recvThread.start()                                          
    sendMsgThread.start()                                       
    sendOnlineThread.start()                                    
    recvThread.join()                                           
    sendMsgThread.join()                                        
    sendOnlineThread.join()                                     

if __name__ == '__main__':
    main()

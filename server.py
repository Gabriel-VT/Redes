import socket
import select

HEADER_LENGTH = 10

class Server:
    def __init__(self):
        self.__ip=socket.gethostbyname(socket.gethostname())
        self.__port=2000
        self.__reg=open('message_log.txt', 'a+')
        self.__clients={}
        self.__sockets_list=[]
        self.__server_socket=""
    
    def open(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server_socket.bind((self.__ip, self.__port))
        self.__server_socket.listen()
        self.__sockets_list = [self.__server_socket]
        print(f'Listening for connections on :{self.__port}...')
        self.__reg.write(u'Aguardando conexão' + '\n')

    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(HEADER_LENGTH)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())
            return {'header': message_header, 'data': client_socket.recv(message_length)}

        except:
            return False
    
    def start(self):
        print(f'Listening for connections on :{self.__port}...')
        self.__reg.write(u'Aguardando conexão' + '\n') 

        while True:
            read_sockets, _, exception_sockets = select.select(self.__sockets_list, [], self.__sockets_list)
            
            for notified_socket in read_sockets:
                if notified_socket == self.__server_socket:
                    client_socket, client_address = self.__server_socket.accept()
                    user = self.receive_message(client_socket)

                    if user is False:
                        continue

                    self.__sockets_list.append(client_socket)
                    self.__clients[client_socket] = user

                    print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf8')))
                    self.__reg.write('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf8')))
                
                else:

                    message = self.receive_message(notified_socket)

                    if message is False:
                        print('Closed connection from: {}'.format(self.__clients[notified_socket]['data'].decode('utf-8')))
                        self.__reg.write('Closed connection from: {}'.format(self.__clients[notified_socket]['data'].decode('utf-8')))
                        sockets_list.remove(notified_socket)
                        del self.__clients[notified_socket]
                        continue

                    user = self.__clients[notified_socket]
                    print(f'Received message from {user["data"]}: {message["data"].decode("utf-8")}')
                    self.__reg.write(f'Received message from {user["data"]}: {message["data"].decode("utf-8")}')

                    for client_socket in self.__clients:
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                            
            for notified_socket in exception_sockets:
                print('Closed connection from: {}'.format(self.__clients[notified_socket]['data'].decode('utf-8')))
                self.__reg.write('Closed connection from: {}'.format(self.__clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del self.__clients[notified_socket]

    def exit(self):
        self.__reg.write('Servidor encerrado')
        self.__reg.close()
        self.__server_socket.close()

    def run(self):
        self.open()
        self.start()

s=Server()
s.run()
import socket, time
import select
import errno


HEADER_LENGTH = 10

class Client:
    def __init__(self):
        self.__port=2000
        self.__ip=""
        self.__user=""
        self.__client_socket=""

    def open(self):
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_socket.connect((self.__ip, self.__port))
        self.__client_socket.setblocking(False)
        time.sleep(0.2)

    def start(self):
        user = self.__user.encode('utf-8')
        user_header = f"{len(user):<{HEADER_LENGTH}}".encode('utf-8')
        self.__client_socket.send(user_header + user)

        while True:

            message = input(f'{self.__user} > ')
            
            if message:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                self.__client_socket.send(message_header + message)

            try:
                while True:
                    user_header = self.__client_socket.recv(HEADER_LENGTH)

                    if not len(user_header):
                        print('Connection closed by the server')
                        sys.exit()

                    user_length = int(user_header.decode('utf-8').strip())
                    user = self.__client_socket.recv(user_length).decode('utf-8')
                    
                    message_header = self.__client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = self.__client_socket.recv(message_length).decode('utf-8')

                    print(f'{user} > {message}')

            except IOError as e:     
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                continue
            except Exception as e:
                print('Reading error: '.format(str(e)))
                sys.exit()

    def run(self):
        self.__ip=input("Server Address: ")
        self.__user=input("Nickname: ")
        self.open()
        self.start()

c=Client()
c.run()
import socket, json, random

end='/end'

class Client:
    def __init__(self):
        self.__client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def open(self, host, port): #open client
        self.__server_addr=(host, port)
        self.__client.connect(self.__server_addr)

    def run(self):
        content=input('message: ')
        message={'content':content, 'list_ex':[1,2,3,4,5],'to':random.randint(1,10), 'num':random.randint(1,10)}

        self.__client.send(json.dumps(message).encode())

        self.__client.send(json.dumps(end).encode())

        from_server=json.loads(self.__client.recv(4096).decode())
        print(from_server)
            
        self.__client.close()
        

ip=socket.gethostbyname(socket.gethostname())
port=2000

c=Client()
c.open(ip, port)
c.run()



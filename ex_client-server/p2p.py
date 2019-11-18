import socket, time
from client import *
from server import *
import _thread as thread

#constants
end='/end'
none='/NA'
close='/cls'

def parse_text(text):
    d={}
    lista=text.split(';')
    for seg in lista:
        div=seg.split('=')
        d[div[0]]=div[1]

    return d

class P2P:
    def __init__(self):
        self.__p2p=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open(self, host, port):
        self.__p2p_addr=(host, port)
        self.__client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self):
        self.__serv.bind(self.__addr)
        self.__serv.listen(5)

        while True:
            conn, addr = self.__serv.accept()
            print('Conectado a '+addr[0])

            while True:
                    #received message
                    data=conn.recv(4096).decode()

                    if not data or data==end: break

                    #parse
                    dic=parse_text(data)
                    print("Recebido:")
                    print(data)
                    print("Conteudo:")
                    print(dic['cont'])
                    print()

                    if end in data: break
                        
            conn.close()

        self.__serv.close()

    def start(self):
        thread.start_new_thread(self.listen, ())
        host, port=self.__p2p_addr

        while True:
            dest=input('Destino ("0" para sair): ')
            dest_addr=(dest, port)
            
            self.__client.connect(dest_addr)

            self.__client.settimeout(1)

            #message content
            content=input('Mensagem: ')
            #format message
            message=str.format("char={};dest={};cont={}",len(content),dest, content)
            #send
            self.__client.send(message.encode())
            self.__client.send(end.encode())

            self.__client.close()

        self.__client.close()
                

        

    def run(self):
        ip=socket.gethostbyname(socket.gethostname())
        print('Seu IP: '+ip)
        port=int(input('Digite a porta: '))

        self.open(ip, port)
        self.start()

        
p=P2P()
p.run()
        

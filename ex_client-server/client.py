import socket, time
import _thread as thread

end='/end'
none='/NA'

def parse_text(text):
    d={}
    lista=text.split(';')
    for seg in lista:
        div=seg.split('=')
        d[div[0]]=div[1]

    return d

class Client:
    def __init__(self):
        #init client
        self.__client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def open(self, host, port):
        #connect to server
        self.__client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_addr=(host, port)
        self.__client.connect(self.__server_addr)
           

    def run(self):
        ip=input('Digite o IP do servidor: ')
        port=int(input('Digite a porta: '))
        self.open(ip, port)

        #set timeout in seconds
        self.__client.settimeout(1)

        #
        while True:
            #open connection
            self.open(ip, port)
            time.sleep(0.2)

            #message destination
            dest=input('Destino ("0" para sair): ')

            if dest!='0':
                #message content
                content=input('Mensagem: ')
                #format message
                message=str.format("char={};dest={};cont={}",len(content),dest, content)
                #send
                self.__client.send(message.encode())
                self.__client.send(end.encode())

                #wait response (with timeout)
                received=[]
                while True:
                    #received message
                    from_server=self.__client.recv(4096).decode()
                    if not from_server or from_server==end: break

                    #if there is messages print
                    if from_server!=none:
                        print("Recebido:")
                        print(from_server)
                        print("Conteudo:")
                        print(parse_text(from_server)['cont'])
                        print()

                self.__client.close()
        
            else:
                break

        self.__client.close()
            
        



c=Client()
c.run()



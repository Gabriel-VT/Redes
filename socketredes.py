import socket, time, functools

def checksum(st):
    return functools.reduce(lambda x,y:x+y, map(ord, st))

class SocketClient:
    def __init__(self):
        self.__client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__buffer=()
        self.__encoding='utf-8'

    def open(self, host, port, timeout=None):
        self.__server_addr=(host, port)
        self.__client.connect(self.__server_addr)
        self.__addr=socket.gethostbyname(socket.gethostname()), port
        self.__client.settimeout(timeout)

    def save(self, filename, content):
        try:
            file= open(filename, 'a')
            file.write(content)
            file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()

    def parse_text(self, text):
        lista=text.split(';\n')
        dic={}
        for i in range(len(lista)):
            if ': ' in lista[i]:
                lista[i]=lista[i].split(': ')
                try:
                    dic[lista[i][0]]=int(lista[i][1])
                except:
                    dic[lista[i][0]]=lista[i][1]
        return dic
            
    def run(self):
        try:
            
            ip=input('digite o IP do servidor: ')
            port=int(input('digite a porta do servidor: '))
            self.open(ip, port)
            self.__buffer=()

            while True:
                destination=input("Digite o destinatário: ")
                content=input("Digite a mensagem: ")
                
                responses=()
                sequence=0
                check=checksum(content)
                    
                print('send')
                header='Sender: '+str(self.__addr)+';\nDestination: '+str(destination)+';\nSeq: '+ str(sequence)+';\nChecksum: '+str(check)+';\nContent: '
                message=header+content+';\n'

                self.__buffer+=(message,)
                self.__client.send(message.encode('utf-8'))
                print('sent')

                from_server=self.__client.recv(4096).decode('utf-8')
                received=self.parse_text(from_server)
                print(from_server)


        except Exception as e:
            print(e)

        finally:
            self.__client.close()

            

        

class SocketServer:
    def __init__(self):
        self.__serv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__encoding='utf-8'

    def open(self, host, port, timeout=None):
        self.__addr=(host, port)
        self.__serv.bind(self.__addr)
        self.__serv.listen(5)
        self.__serv.settimeout(timeout)
        

    def save(self, filename, content):
        try:
            file= open(filename, 'a')
            file.write(content)
            file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()

    def parse_text(self, text):
        lista=text.split(';\n')
        dic={}
        for i in range(len(lista)):
            if ': ' in lista[i]:
                lista[i]=lista[i].split(': ')
                try:
                    dic[lista[i][0]]=int(lista[i][1])
                except:
                    dic[lista[i][0]]=lista[i][1]
        return dic

    def run(self):
        try:
            ip=socket.gethostbyname(socket.gethostname())
            port=int(input('digite a porta do servidor: '))
            self.open(ip, port)
            print("Servidor aberto em "+ip+" na porta "+str(port))
            self.__buffer=()
            while True:
                conn, client_addr = self.__serv.accept()
                from_client=''

                sequence=0
                while True:
                    data=conn.recv(4096).decode('utf-8')
                    if not data: break
                    from_client+=data
                    received=self.parse_text(from_client)
                    if checksum(received['Content'])==received['Checksum']:
                        conn.send(('ACK '+str(received['Seq'])).encode('utf-8'))
                    else:
                        conn.send('NAK '.encode('utf-8'))

                print(from_client)

                received=self.parse_text(from_client)
                print(received)
                    
                ack=0
                content='0'
                check=checksum(content)
                header='Sender: '+str(self.__addr)+';\nDestination: '+str(client_addr)+';\nSeq: '+ str(sequence)+';\nChecksum: '+str(check)+';\nContent: '
                message=header+content+';\n'
                    
                conn.send(message.encode('utf-8'))

                sequence+=1
                
                #break


        except Exception as e:
            print(e)
            
        finally:
            conn.close()
            print('desconectado')


class P2P:
    def __init__(self):
        pass
        

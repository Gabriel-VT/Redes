import socket, time, functools, json, deepcopy
MAX_SIZE=100

CONTENT_HEADER='Content'
SENDER_HEADER='Sender'
DEST_HEADER='Destination'
CONT_HEADER='Content'
SEQ_HEADER='Seq'
CHECKSUM_HEADER='Checksum'
MSG_HEADER='MESSAGE'
ACK_HEADER='ACK'
REQUEST_HEADER='REQUEST'


def checksum(st):
    return functools.reduce(lambda x,y:x+y, map(ord, st))

class SocketClient:
    def __init__(self):
        self.__client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__buffer=()
        self.__encoding='utf-8'

    def open(self, host, port, timeout=None): #open client
        self.__server_addr=(host, port)
        self.__client.connect(self.__server_addr)
        self.__addr=socket.gethostbyname(socket.gethostname()), port
        self.__client.settimeout(timeout)

    def save(self, filename, content): #save in file
        try:
            file= open(filename, 'a')
            file.write(content)
            file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()
            
    def run(self): #start
        try:
            #CONNECT TO THE HOST
            ip=input('digite o IP do servidor: ')
            port=int(input('digite a porta do servidor: '))
            self.open(ip, port)
            self.__buffer=[]
            print('Seu IP: '+socket.gethostbyname(socket.gethostname()))

            while True:
                #REQUEST MESSAGE TO BE SENT AND THE DESTINATION
                destination=input("Digite o IP do destinatário: ")
                content=input("Digite a mensagem: ")

                #CUT MESSAGE INTO PIECES
                size=len(content)
                quant=size//MAX_SIZE
                if size%MAX_SIZE!=0:
                    quant+=1
                for sequence in range(quant):
                    if sequence!=quant-1:
                        c=content[sequence*MAX_SIZE:(sequence+1)*MAX_SIZE]
                    else:
                        c=content[sequence*MAX_SIZE:]

                    #CHECKSUM
                    check=checksum(c)

                    #GENERATE MESSAGE DICT
                    print('send')
                    message={CONTENT_HEADER:c, SENDER_HEADER:self.__addr[0], DEST_HEADER: destination, SEQ_HEADER: sequence, CHECKSUM_HEADER: check, REQUEST_HEADER: True, ACK_HEADER: []}

                    #ADD TO BUFFER AND SEND
                    self.__buffer.append(message)
                    self.__client.send(json.dumps(message).encode(self.__encoding))
                    print('sent')

                #ENDED SENDING
                self.__client.send(json.dumps(CONTENT_END).encode(self.__encoding))
                print('end')


                #WAIT RESPONSE
                from_server=''
                while True:
                    data=self.__client.recv(4096).decode(self.__encoding)
                    #print(data)
                    if not data or data==CONTENT_END: break
                    from_server+=data
                    if CONTENT_END in from_server: break

                #RECEIVED RESPONSE
                received=json.loads(from_server)
                print('RECV')
                print(received)

                #ACKs
                acklist=[]
                if checksum(received[CONTENT_HEADER])==received[CHECKSUM_HEADER]:
                    acklist.append(received[SEQ_HEADER])
                    messages.append(received)
                    print('ack')
                else:
                    print('nak')

                #SEND ACKS
                send=[]
                for m in messages:
                    m[ACK_HEADER]=acklist

                    if m[DEST_HEADER]==client_addr[0]:
                        #IF REQUEST SEND MESSAGES AND ACKS
                        if received[REQUEST_HEADER]:
                            send.append(m)
                            
                        #IF NOT REQUEST SEND ONLY ACKS
                        else:
                            ackmessage=m.deepcopy()
                            ackmessage[CONTENT_HEADER]=ACK_HEADER
                            send.append(ackmessage)
                    


        except Exception as e:
            print('erro')
            print(e)

        finally:
            self.__client.close()

            

        

class SocketServer:
    def __init__(self):
        self.__serv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__encoding='utf-8'

    def open(self, host, port, timeout=None): #open client
        self.__addr=(host, port)
        self.__serv.bind(self.__addr)
        self.__serv.listen(5)
        self.__serv.settimeout(timeout)
        

    def save(self, filename, content): #save in file
        try:
            file= open(filename, 'a')
            file.write(content)
            file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()

    def run(self): #start
        try:
            #OPEN SERVER AT LOCALHOST AND SELECTED PORT
            ip=socket.gethostbyname(socket.gethostname())
            port=int(input('digite a porta do servidor: '))
            self.open(ip, port)
            print("Servidor aberto em "+ip+" na porta "+str(port))
            self.__buffer=[]
            recv_messages=[]
            
            while True:
                #WAIT CONNECTION
                conn, client_addr = self.__serv.accept()
                print('Conectado a '+client_addr[0])
                from_client=''

                #WAIT MESSAGE
                while True:
                    data=conn.recv(4096).decode(self.__encoding)
                    #print(data)
                    if not data or data==CONTENT_END: break
                    from_client+=data
                    if CONTENT_END in from_server: break

                #RECEIVED MESSAGE
                received=json.loads(from_client)
                print('RECV')
                print(received)

                #ACKs
                acklist=[]
                if checksum(received[CONTENT_HEADER])==received[CHECKSUM_HEADER]:
                    acklist.append(received[SEQ_HEADER])
                    messages.append(received)
                    print('ack')
                else:
                    print('nak')

                #GENERATE RESPONSE AND ADD TO BUFFER
                print(messages)

                for m in messages:
                    m[ACK_HEADER]=acklist

                    if m[DEST_HEADER]==client_addr[0]:
                        #IF REQUEST SEND MESSAGES AND ACKS
                        if received[REQUEST_HEADER]:
                            self.__buffer.append(m)
                            
                        #IF NOT REQUEST SEND ONLY ACKS
                        else:
                            ackmessage=m.deepcopy()
                            ackmessage[CONTENT_HEADER]=ACK_HEADER
                            self.__buffer.append(ackmessage)

                #CUT MESSAGE INTO PIECES
                size=len(content)
                quant=size//MAX_SIZE
                if size%MAX_SIZE!=0:
                    quant+=1
                for sequence in range(quant):
                    if sequence!=quant-1:
                        c=content[sequence*MAX_SIZE:(sequence+1)*MAX_SIZE]
                    else:
                        c=content[sequence*MAX_SIZE:]

                    #CHECKSUM
                    check=checksum(c)

                    #GENERATE MESSAGE DICT
                    print('send')
                    message={CONTENT_HEADER:c, SENDER_HEADER:self.__addr[0], DEST_HEADER: destination, SEQ_HEADER: sequence, CHECKSUM_HEADER: check, REQUEST_HEADER: False, ACK_HEADER: []}

                    #ADD TO BUFFER AND SEND
                    self.__client.send(json.dumps(message).encode(self.__encoding))
                    print('sent')

                #ENDED SENDING
                self.__client.send(json.dumps(CONTENT_END).encode(self.__encoding))
                print('end')


                #WAIT ACKs

                    


        except Exception as e:
            print('erro')
            print(e)
            
        finally:
            conn.close()
            print('desconectado')
        

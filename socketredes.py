import socket, time, json


class SocketClient:
    def __init__(self):
        self.__client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__buffer=()
        self.__encoding='utf-8'

    def open(self, host, port):
        self.__server_addr=(host, port)
        self.__client.connect(self.__server_addr)
        self.__addr=socket.gethostbyname(socket.gethostname()), port

    def send(self, message):
        self.__client.send(json.dumps(message).encode(self.__encoding))

    def receive(self, size=4096):
        return json.loads(self.__client.recv(size).decode(self.__encoding))

    def wait_for_response(self, timeout=2):
        response=self.receive()
        start=time.time()
        elapsed_time=time.time()-start
        
        if not self.__response and elapsed_time<timeout:
            elapsed_time=time.time()-start
            response=self.receive()
            print('wait')

        return response

    def close(self):
        self.__client.close()

    def save(self, filename, content):
        try:
            file= open(filename, 'a')
            file.write(content)
            file.write('\n')
        except Exception as e:
            print(e)
        finally:
            file.close()

    '''def parse_text(self, text):
        
        return lista'''
            
    def run(self):
        try:
            sequence=0
            ip=input('digite o IP do servidor: ')
            port=int(input('digite a porta do servidor: '))
            self.open(ip, port)
            
            while True:
                content=input("Digite a mensagem terminando com ';': ")
                
                if content[-1]!=';':
                    content+=';'
                
                check=0
                message={"content":content, "sequence":sequence, "sender":self.__addr, "destination":self.__server_addr, 'checksum':check}
                self.save("client.txt","SENT: " + str(message))
                sequence+=1
                self.__buffer+=(message,)

                print(message)

                for m in self.__buffer:
                    self.send(m)
                    print("sending")
                
                response=self.wait_for_response()
                self.__response=0

                print('RESPOSTA: '+str(response))

                if response!='':
                    self.save("client.txt","RESPONSE: " + str(response))
                    response=self.parse_text(response)
                    for line in response:
                        line=line.split()
                        
                        if 'ACK'==line[0]:
                            while i in range(self.__sent):
                                if str(self.__buffer[i].sequence()) in line:
                                    del self.__buffer[i]
                                else:
                                    i+=1
                else:
                    self.save("client.txt","RESPOSTA INVALIDA: " + str(response))


        except Exception as e:
            print(e)

        finally:
            self.close()

            

        

class SocketServer:
    def __init__(self):
        self.__serv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__encoding='utf-8'

    def open(self, host, port):
        self.__addr=(host, port)
        self.__serv.bind(self.__addr)
        self.__serv.listen(5)

    def wait(self, size=4096):
        while True:
            print('aguardando')
            conn, client_addr = self.__serv.accept()
            print('aceito')
            from_client=()
            receivednum=()

            try:

                while True:
                    data=json.loads(conn.recv(size).decode(self.__encoding))

                    if data == {}:
                        print('nada')
                        break
                    else:
                        print('data')
                        print(data)

                    check=0 #calcular

                    if data['checksum']==check:
                        from_client+=(data,)
                        receivednum+=(data['sequence'],)
                        print('check')
                        break

                numbers=str(receivednum).replace(',',' ').replace('(', '').replace(')','')
                ack={"content":"ACK: "+ numbers + ";", "sequence":-1, "sender":self.__addr, "destination":client_addr}    
                print('sending')
                conn.send(json.dumps(ack).encode(self.__encoding))
                print('close1')
                conn.close()
                print('close2')

            except Exception as e:
                print(e)
                print('wait func')

            finally:
                conn.close()

            if from_client!=():
                print('return')
                return from_client, ack

    def send(self, message):
        pass

    def close(self):
        self.__serv.close()

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
        lista=text.split(';')
        return lista

    def run(self):
        try:
            #ip=input('digite o IP do servidor: ')
            ip=socket.gethostbyname(socket.gethostname())
            port=int(input('digite a porta do servidor: '))
            self.open(ip, port)
            print("Servidor aberto em "+ip+" na porta "+str(port))
            while True:
                print("AGUARDANDO MENSAGEM")
                messages, ack =self.wait()

                for m in messages:
                    print("RECEBIDO: "+str(m))
                    self.save("server.txt","RECEIVED: "+str(m))
                print("ACKS ENVIADOS: "+str(ack))
                self.save("server.txt","SENT ACKs: "+str(ack))

        except Exception as e:
            print(e)
            
        finally:
            self.close()

class P2P:
    def __init__(self):
        pass
        

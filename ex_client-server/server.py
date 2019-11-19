import socket, time
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

class Server:
    def __init__(self):
        #init server
        self.__serv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open(self, host, port):
        #open server at host ip and port
        self.__addr=(host, port)
        self.__serv.bind(self.__addr)
        self.__serv.listen(5)

        #received messages list
        self.__messages=[]

    def start(self):
        while True:
            #wait connection from client
            conn, addr = self.__serv.accept()
            print('Conectado a '+addr[0])

            close_cmd=0
            while True:
                #received message
                data=conn.recv(4096).decode()

                if not data or data==end: break
                
                if data == close:
                    close_cmd=1
                    break

                #save in list
                self.__messages.append(data)
                print(data)

                #parse
                dic=parse_text(data)
                
                #send corresponding messages to client
                count=0
                i=0
                while i < len(self.__messages):
                    msg=self.__messages[i]
                    dest=parse_text(msg)['dest']
                    if dest == addr[0]:
                        count+=1
                        conn.send(msg.encode())
                        del self.__messages[i]
                        time.sleep(0.2)
                    else:
                        i+=1
                        
                #if no messages have been found, send '/NA'
                if count==0:
                    conn.send(none.encode())

                if end in data: break
                    
            conn.close()

            if close_cmd==1: break

        self.__serv.close()
        
        
    def run(self):
        ip=socket.gethostbyname(socket.gethostname())
        print('Seu IP: '+ip)
        port=int(input('Digite a porta: '))

        self.open(ip,port)
        self.start()
        
s=Server()
s.run()
        


        

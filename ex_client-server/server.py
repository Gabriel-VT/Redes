import socket, time
import _thread as thread

end='/end'
ack='/ACK'
none='/NA'

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

    def on_new_client(self, clientsocket, addr): 
        while True:
            #received message
            data=clientsocket.recv(4096).decode()

            if not data or data==end: break

            #save in list
            self.__messages.append(data)
            print(data)

            #parse
            dic=parse_text(data)
            
            #send corresponding messages to client
            count=0
            for msg in self.__messages:
                dest=parse_text(msg)['dest']
                if dest == addr[0]:
                    count+=1
                    clientsocket.send(msg.encode())
                    time.sleep(0.2)
                    
            #if no messages have been found, send '/NA'
            if count==0:
                clientsocket.send(none.encode())

            if end in data: break
                
        clientsocket.close()

    def run(self):
        while True:
            #wait connection from client
            conn, addr = self.__serv.accept()
            print('connected to '+addr[0])

            #open thread
            thread.start_new_thread(self.on_new_client, (conn, addr))

        self.__serv.close()
        

ip=socket.gethostbyname(socket.gethostname())
port=2000

s=Server()
s.open(ip,port)
s.run()



        

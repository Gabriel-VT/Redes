import socket, json, random

end='/end'

class Server:
    def __init__(self):
        self.__serv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open(self, host, port):
        self.__addr=(host, port)
        self.__serv.bind(self.__addr)
        self.__serv.listen(5)

    def run(self):
        messages=[]
        while True:
            conn, addr = self.__serv.accept()
            print('connected to '+addr[0])

            while True:
                data=json.loads(conn.recv(4096).decode())
                if not data or data==end: break
                print('receiving')
                print(data)
                messages.append(data)

            send=[]
            r=random.randint(1,10)
            print(r)
            for m in messages:
                if m['num']==r:
                    send.append(m)
                
            conn.send(json.dumps(send).encode())

            conn.send(json.dumps(end).encode())

            conn.close()
            print('disconnected')
        

ip=socket.gethostbyname(socket.gethostname())
port=2000

s=Server()
s.open(ip,port)
s.run()



        

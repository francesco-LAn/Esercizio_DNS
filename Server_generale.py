import asyncio.streams
import json,time

NAME_PORT = 6000
TIME_PORT = 6001
ECHO_PORT = 6002
host = "127.0.0.1"


class Name_server():
    diz_servizi = {"time":[host,TIME_PORT],"echo":[host,ECHO_PORT]}

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    async def gestione_client(self,reader,writer):
        pass


class Time_server():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    async def gestione_client(self,reader,writer):
        pass


class Echo_server():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    async def gestione_client(self,reader,writer):
        pass


async def avvio(server):                #Ogni task eseguira questo
   s = await asyncio.start_server(server.gestione_client,server.ip,server.port)
   print(f"Server {server.port} partito")
   async with s:
    await s.serve_forever()              #Ogni task (ognuna delle quali corrisponde ad un server) rimane qui 
  

async def run(lista):           #Prima funzione: crea 3 task, una per ogni Server
    lista_task = []
    for server in lista:
        t = asyncio.create_task(avvio(server))          #Crea la task che deve eseguire l'altra funzione
        lista_task.append(t)

    await asyncio.gather(*lista_task)           #Con l'asterisco considero tutti i componenti


  # MAIN
server_name = Name_server(host,NAME_PORT)
server_time = Time_server(host,TIME_PORT)
server_echo = Echo_server(host,ECHO_PORT)     
lista_server = [server_name,server_echo,server_time]

try:
    asyncio.run(run(lista_server))        #Faccio partire i 3 server

except KeyboardInterrupt:
    print("Server chiuso")

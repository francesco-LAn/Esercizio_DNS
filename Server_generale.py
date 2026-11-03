import asyncio.streams
import json,time

NAME_PORT = 6000
TIME_PORT = 6001
ECHO_PORT = 6002
host = "127.0.0.1"

class Struttura_server:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    async def gestione_client(self,reader,writer):
        try:
            while True:
                richiesta = await reader.readline()         #Attende una richiesta da parte del client
                
                if richiesta:
                    try:
                        dati_leggibili = json.loads(richiesta.decode())

                        risposta_pronta = await self.elaborazione_dati(dati_leggibili)

                        await self.invia_messaggio(writer,risposta_pronta) #*Terminato tutto invia al client la risposta, con lo \n

                    #Se si verificano Eccezzioni
                    except json.decoder.JSONDecodeError:
                        print("Errore di lettura formato JSON, server ancora attivo")
                        risposta = {"status": "error", "message": "SERVIZIO INESISTENTE"}       #Invia in caso di errore di json
                        await self.invia_messaggio(writer,risposta)

                    except (KeyError, TypeError):
                        print("Errore formato richiesta")
                        risposta = {"status": "error", "message": "CAMPO MANCANTE"}       #Invia in caso di errore di json
                        await self.invia_messaggio(writer,risposta)                    

                else:      #Caso di richiesta uguale a vuoto b''
                    break
                
        except ConnectionRefusedError:
            pass

        finally:
            writer.close()
            await writer.wait_closed()


    async def invia_messaggio(self,writer,messaggio):
        writer.write( (json.dumps(messaggio)+'\n').encode() )
        await writer.drain()


    async def elaborazione_dati(self,dati_leggibili):
        ##Funzione che riceve i dati e elabora la risposta da inviare
        #Deve ritornare la rispota pronta
        pass



##CLASSE NAME SERVER ---------------------------------------------------------------------------------------------
class Name_server(Struttura_server):
    diz_servizi = {"time":{"host":host,"porta":TIME_PORT},"echo":{"host":host,"porta":ECHO_PORT}}   

    #Metodi: INIT , gestione_client e invio_messaggi possono non essere sovrascritti 

    async def elaborazione_dati(self,dati_leggibili):
        #!SE DESSE ERRORE SAREBBE UN KEY-ERROR, GESTITO IN UN EXCEPT
        if dati_leggibili["cmd"] == "lookup":               #Verifico che sia stata inviata la richiesta in formato giusto per questo server

            servizio_richiesto = dati_leggibili["service"]
            if servizio_richiesto in self.diz_servizi:
                #*RISPOSTA viene creata automaticamente in base al servizio richiesto, anche se avessi 100 servizi (con la stessa struttura) funzionerebbe
                risposta = {"status": "ok", "service": servizio_richiesto,
                "host": self.diz_servizi[servizio_richiesto]["host"], "port": self.diz_servizi[servizio_richiesto]["porta"]}                                

            else:  #!Se invece non esiste quel servizio nella lista
                risposta =  {"status": "error", "message": "SERVIZIO INESISTENTE"}      

        elif dati_leggibili["cmd"] == "list":
            servizi = []
            for servizio in self.diz_servizi:       #Scorre tutte le chiavi del dizionario che contiene i servizi
                servizi.append(servizio)           #Li aggiunge agli elementi della lista

            risposta = risposta =  {"status": "ok", "servizi": servizi}

        else:                                       #Se cmd è diverso da questi: allora da errore
            risposta =  {"status": "error", "message": "COMANDO INESISTENTE"}

        return risposta #QUALUNQUE SIA LA RISPOSTA viene ritornata alla funzione principale



##CLASSE TIME SERVER ---------------------------------------------------------------------------------------------
class Time_server(Struttura_server):

    async def elaborazione_dati(self,dati_leggibili):
        #!SE DESSE ERRORE SAREBBE UN KEY-ERROR, GESTITO IN UN EXCEPT
        if dati_leggibili["cmd"] == "time":               #Verifico che sia stata inviata la richiesta in formato giusto per questo server
            data_e_ora = time.strftime("%d/%m/%Y %H:%M:%S")
            risposta = {"status": "ok", "time": data_e_ora}

        else:
            risposta =  {"status": "error", "message": "SERVIZIO INESISTENTE"}

        return risposta

##CLASSE ECHO SERVER ---------------------------------------------------------------------------------------------
class Echo_server(Struttura_server):

    async def elaborazione_dati(self,dati_leggibili):
        #!SE DESSE ERRORE SAREBBE UN KEY-ERROR, GESTITO IN UN EXCEPT
        if dati_leggibili["cmd"] == "echo":               #Verifico che sia stata inviata la richiesta in formato giusto per questo server
            risposta = {"status": "ok", "text": dati_leggibili["text"]}

        else:
            risposta =  {"status": "error", "message": "SERVIZIO INESISTENTE"}

        return risposta


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
    print("Ogni server è stato chiuso")

import asyncio
import argparse,json

parser = argparse.ArgumentParser(description="Client che comunica con diversi server e servizi, tra cui un simil DNS")      #Creo l'oggetto argparse per leggere la linea di comando

#*Settaggio dei valori richiesti all'avvio del programma:
parser.add_argument("ip", help="indirizzo IP del server host")         
parser.add_argument("servizio",help="nome del servizio richiesto")
parser.add_argument("--messaggio",default='default', help="valore facoltativo e non, in base al servizio scelto") #Il messaggio da inviare

#default serve a rendere opzionale un campo, cioè se non viene inserito viene usato quel valore di default
# -- rende facoltativo messaggio così da non dare errore
#Con -h ottengo le descrizioni qui scritte in help

args = parser.parse_args()      #Faccio partire l'esecuzione del parser
PORTA = 6000
ip = args.ip
servizio = args.servizio                #Può essere: 'time - 'echo'
messaggio = args.messaggio


async def main():
    #Prima di aprire la comunicazione controllo il comando
    if servizio ==  'time':
        if messaggio != "default":              #Il campo messaggio deve essere vuoto in questo caso
            print("Errore di sintassi comando, messaggio non necessario!")
            writer.close()    #!Chiusura client
            return   
    try:
        reader, writer = await asyncio.open_connection(ip,PORTA)            #Il client conosce solo questa porta, quindi si connette a lui di base, poi le altre le deve richiedere
        
        #Se per caso il servizio non esiste, viene inviato lo stesso poi sarà il server a dare ERRORE
        richiesta = {"cmd":"lookup","service":servizio}     
    
        risposta_leggibile = await invio_richieste(writer,reader,richiesta)        #*1 INVIO ----------------------------------------

        if risposta_leggibile['status'] == 'ok':
            porta_ottenuto = risposta_leggibile['port']
            ip_ottenuto = risposta_leggibile["host"]
            reader2, writer2 = await asyncio.open_connection(ip_ottenuto,porta_ottenuto)

            if servizio == "echo":
                richiesta = {"cmd": "echo","text": messaggio}
            
            else:
                richiesta = {"cmd": "time"}

            #2 INVIO --------------------------------------------------------
            risposta_leggibile = await invio_richieste(writer2,reader2,richiesta)

            if risposta_leggibile['status'] == 'ok':
                if servizio == "time":
                    print(risposta_leggibile["time"])
                else:
                    print(risposta_leggibile["text"])

            else:  #Caso di STATUS errato
                print(risposta_leggibile["message"])

            writer2.close()


        else:       #Caso di STATUS errato
            print(risposta_leggibile["message"])
    
    except ConnectionError:
        print("Errore di connessione")

    finally:
        writer.close()



async def invio_richieste(writer,reader,messaggio):
    writer.write( (json.dumps(messaggio)+"\n").encode() )
    await writer.drain()
    risposta = await reader.readline()

    return json.loads(risposta.decode())        #Ritorna la riposta in formato leggibile
    


asyncio.run(main())
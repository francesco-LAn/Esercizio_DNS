import asyncio
import argparse,json

parser = argparse.ArgumentParser(description="Client publisher: invia un messaggio a un topic del broker")      #Creo l'oggetto argparse per leggere la linea di comando

#*Settaggio dei valori richiesti all'avvio del programma:
parser.add_argument("ip", help="indirizzo IP del broker")               #Il broker, cioè l'indirizzo          
parser.add_argument("porta", help="topic a cui si riferisce il messaggio")  # Il topic di riferimento per l'invio
parser.add_argument("messaggio", help="testo del messaggio (tra virgolette se contiene spazi)") #Il messaggio da inviare
#Con -h ottengo le descrizioni qui scritte in help

args = parser.parse_args()      #Faccio partire l'esecuzione del parser

ip = args.ip
porta = args.porta
messaggio = args.messaggio

async def main(broker,topic,messaggio):
    reader, writer = await asyncio.open_connection(ip,porta)
    #Fare sequenza di case o switch, in base alla porta

    #messaggi_invio = {"cmd":}
    writer.write(json.dumps("") )
    await writer.drain()

    writer.close()


asyncio.run(main(broker,topic,messaggio))
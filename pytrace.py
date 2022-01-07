import sys
import socket
import random
from datetime import datetime
tempos = []


def traceroute(endereco_destino, pulos_maximos=30, tempo_limite=0.9):
    proto_icmp = socket.getprotobyname('icmp')
    proto_udp = socket.getprotobyname('udp')
    porta = random.choice(range(33434, 33535))

    for ttl in range(1, pulos_maximos+1):

        inicioTime = datetime.now()  
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto_icmp)
        receiver.settimeout(tempo_limite)
        receiver.bind(('', porta))
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto_udp)
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)    
        sender.sendto(b'', (endereco_destino, porta))

        try:
            dados, endereco_atual = receiver.recvfrom(512)
            endereco_atual = endereco_atual[0]
           
        except socket.error:
            endereco_atual = None

        finally:
            tempoTotal = datetime.now() - inicioTime
            tempos.append(tempoTotal)
            receiver.close()
            sender.close()

        yield endereco_atual

        if endereco_atual == endereco_destino:
            break


if __name__ == "__main__":

    url_destino = sys.argv[1]
    endereco_destino = socket.gethostbyname(url_destino)
    print("Traceroute para %s (%s)" % (url_destino, endereco_destino))
    print('\nhop\taddr\t\ttotal_time')

    for i, v in enumerate(traceroute(endereco_destino)):

        if v is None:
            print(str(i+1) + '\tNão foi possível enviar o pacote para o endereço.')
        else:
            print(str(i+1) + "\t" + str(v) + "\t" + str(tempos[i]).split('.')[1] + ' ms')
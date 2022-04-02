import socket
import logging
import json
import ssl

alldata = dict()
alldata['1']=dict(nomor=1, nama="Koko Trikoro")
alldata['2']=dict(nomor=2, nama="Bayu Hermanto")
alldata['3']=dict(nomor=3, nama="Fery Muriadi")
alldata['4']=dict(nomor=4, nama="Deden Muden")
alldata['5']=dict(nomor=5, nama="Harry Maguire")
alldata['6']=dict(nomor=6, nama="Reynald Dean")
alldata['7']=dict(nomor=7, nama="Bambang Pamungkas")
alldata['8']=dict(nomor=8, nama="Tony Probo")
alldata['9']=dict(nomor=9, nama="Paulo Rodiguez")
alldata['10']=dict(nomor=10, nama="Edi Suradi")
alldata['11']=dict(nomor=11, nama="Farhan Gunawan")
alldata['12']=dict(nomor=21, nama="Elmo Street")
alldata['13']=dict(nomor=13, nama="Thoriq Kurniawan")
alldata['14']=dict(nomor=14, nama="Lionel Messi")
alldata['15']=dict(nomor=15, nama="Cristiano Ronaldo")
alldata['16']=dict(nomor=16, nama="Rery Tury")
alldata['17']=dict(nomor=17, nama="Heru Fernandes")
alldata['18']=dict(nomor=18, nama="Tata Ronanda")
alldata['19']=dict(nomor=19, nama="Bruno Mars")
alldata['20']=dict(nomor=20, nama="Danny McClan")

def version():
    return "version 0.0.1"


def process_request(request_string):
    #format request
    # NAMACOMMAND spasi PARAMETER
    cstring = request_string.split(" ")
    result = None
    try:
        command = cstring[0].strip()
        if (command == 'get_player_data'):
            # getdata spasi parameter1
            # parameter1 harus berupa nomor pemain
            logging.warning("getdata")
            nomor_player = cstring[1].strip()
            try:
                logging.warning(f"data {nomor_player} ketemu")
                result = alldata[nomor_player]
            except:
                result = None
        elif (command == 'version'):
            result = version()
    except:
        result = None
    return result

def serialization(a):
    #print(a)
    #serialized = str(dicttoxml.dicttoxml(a))
    serialized =  json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized

def run_server(server_address):
    #--- INISIALISATION ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1000)

    while True:
        # Wait for a connection
        logging.warning("waiting for a connection")
        connection, client_address = sock.accept()
        logging.warning(f"Incoming connection from {client_address}")
        # Receive the data in small chunks and retransmit it

        try:
            complete=False
            data_received="" #string
            while True:
                data = connection.recv(32)
                logging.warning(f"received {data}")
                if data:
                    data_received += data.decode()
                    if "\r\n\r\n" in data_received:
                        complete=True

                    if (complete==True):
                        result = process_request(data_received)
                        logging.warning(f"process result: {result}")

                        #result bisa berupa tipe dictionary
                        #harus diserialization dulu sebelum dikirim via network
                        # Send data
                        # some data structure may have complex structure
                        # how to send such data structure through the network ?
                        # use serialization
                        #  example : json, xml

                        # complex structure, nested dict
                        # all data that will be sent through network has to be encoded into bytes type"
                        # in this case, the message (type: string) will be encoded to bytes by calling encode

                        result = serialization(result)
                        result += "\r\n\r\n"
                        connection.sendall(result.encode())
                        complete = False
                        data_received = ""  # string
                        break

                else:
                   logging.warning(f"no more data from {client_address}")
                   break
            # Clean up the connection
        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 14000))
    except KeyboardInterrupt:
        logging.warning("Control-C: Program shutdown")
        exit(0)
    finally:
        logging.warning("complete")
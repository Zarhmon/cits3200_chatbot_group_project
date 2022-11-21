import socket
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import getopt
import sys
import struct
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(
#     "/etc/letsencrypt/live/cits3200api.zachmanson.com/fullchain.pem",
#     "/etc/letsencrypt/live/cits3200api.zachmanson.com/privkey.pem"
# )


# Sends packed big endian message 
def send_msg(sock, msg):
    if type(msg) == bytes:
        packed_msg = struct.pack('>I', len(msg)) + msg
    else:
        packed_msg = struct.pack('>I', len(msg)) + msg.encode()
    sock.send(packed_msg)

# Receives a packed bid endian message from a socket
def recv_msg(sock):
    packed_msg_len = force_recv_all(sock, 4)
    if not packed_msg_len:
        return None
    try:
        msg_len = struct.unpack('>I', packed_msg_len)[0]
    except struct.error:
        raise Exception("struct error")
    recved_data = force_recv_all(sock, msg_len)
    return recved_data

# Ensures that all the bytes we want to read on receival are read
def force_recv_all(sock, msg_len):
    all_data = bytearray()
    while len(all_data) < msg_len:
        packet = sock.recv(msg_len - len(all_data))
        if not packet:
            return None
        all_data.extend(packet)
    return all_data


# Checks to see if the "-v" flag was used
optlist, args = getopt.getopt(sys.argv[1:], "v")
verbose = False
for opt in optlist:
    if opt[0] == "-v":
        verbose = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if verbose: print("Opened server")
if verbose: print("Created socket")

chatbot = ChatBot("Bot1")
conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]

trainer = ListTrainer(chatbot)
trainer.train(conversation)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

nconnections = 0
# Default values
port = 8888
addr = "0.0.0.0"
# Bind the socket to a port
s.bind((addr, port))
if verbose: print(f"Socket binded to {port}")

# Have the socket listen for a connection
s.listen(5)
if verbose: print("Socket is listening")
s.settimeout(0.1)

try:
    while True:
        try:
            # Accepts a connection
            connection, addr = s.accept()
        except socket.timeout:
            connection = None

        # If a connection has been made
        if connection is not None:
            nconnections +=1
            if verbose: print(f"Got connection {nconnections} from {addr}")
            try:
                received_data = recv_msg(connection).decode()
            except (Exception, socket.timeout):
                if verbose: print("\tClosing connection")
                connection.close()
                continue
            if verbose: print("\t<--",received_data)
            reply = chatbot.get_response(received_data)
            if verbose: print("\t-->",reply)
            send_msg(connection, str(reply))
            
            if verbose: print("\tClosing connection")
            connection.close()

# To close the server ("^C")
except KeyboardInterrupt:
    s.close()
    if verbose: print("\tClosed server")

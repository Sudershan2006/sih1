import shlex
import subprocess
import paramiko
import getpass
import os
import logging
import pickle
import firewall
import threading
from netfilterqueue import NetfilterQueue
from getmac import get_mac_address

def establish_connection(addr, port, user, password):
    """Establish an SSH connection to the specified address and port."""
    client = paramiko.SSHClient()
    pkey = paramiko.RSAKey.from_private_key_file("/home/kali/.ssh/id_rsa",password="Sudershan@98421")
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(addr, username=user,password=password,port=port)
        chan = client.get_transport().open_session()
        return client,chan
    except paramiko.AuthenticationException as e:
        logging.error(f"Authentication failed: {e}")
        return None

def send_command(chan, command):
    """Send a command over the established SSH connection."""
    try:
        chan.send(command)
        output = chan.recv(10240).decode()
        return output
    except Exception as e:
        logging.error(f"Error sending command: {e}")
        return None

def receive_output(ssh_session):
    """Receive output from the SSH session."""
    try:
        output = ssh_session.recv(4096).decode()
        return output
    except Exception as e:
        logging.error(f"Error receiving output: {e}")
        return None
    
def serialize_packet(packet):
    # Create a dictionary to hold packet information
    packet_data = {
        'payload': packet.get_payload(),
        'hw_protocol': packet.hw_protocol,
        'hook': packet.hook,
        'mark': packet.mark,
        'indev':packet.indev ,
        'outdev':packet.outdev,
        'physindev':packet.physindev ,
        'physoutdev':packet.physoutdev,
        'id': packet.id
        # Add other relevant attributes as needed
    }
    
    # Serialize the packet data using pickle
    return pickle.dumps(packet_data)
    
nf = NetfilterQueue()
chan = ''


def process_packet(packet):
    if chan:
        print("Sent....")
        try:
             serialized_packet = serialize_packet(packet)
             chan.send(serialized_packet)
        except Exception as e:
            print(e)
        print(packet)



# def main():
#     user = "kali"
#     password = "kali"
#     ip = '192.168.232.70'
#     port = 22

#     global chan
#     client,chan = establish_connection(ip, port, user, password)
#     if client:
#         print("Communicating with server")
#         output = send_command(chan,'Client connected!')
#         print(output)
#         chan.send(getpass.getuser())
#         chan.send(get_mac_address())
#         print(chan.recv(1024).decode())
#         # firewall.main()
#         # nf.bind(0,process_packet)
#         # try:
#         #     print("Waiting for packets...")
#         #     threading.Thread(target=nf.run).start()
#         # except KeyboardInterrupt:
#         #     nf.unbind()
#         #     # raise 'Exception'
#         #     firewall.flush()
#         #     firewall.list()
#         #     firewall.save_rules()
#         #     raise 'Exception'
#         try:
#             while(True):
#                 print(chan.active)
#                 # packet = firewall.pack
#                 # if packet:
#                 # data = receive_output(chan)
#                 # try:
#                     # if data == 'quit':
#                     #     raise 'Exception'
#                     # chan.send(packet)
#                 pass
#                     # print(chan.active)
                
#         except KeyboardInterrupt as e:
#             chan.close()
#             print(e)
#             print('Client disconnected...')
#             firewall.flush()
#             client.close()
#                 # raise KeyboardInterrupt
        
#             # try:
#             # except Exception as e:
#             #     chan.send(e)
#         # print("hi")

# if __name__ == '__main__':
#     main()

class ServerDownError(Exception) :
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)

def main():
    user = "kali"
    password = "kali"
    ip = '192.168.232.70'
    port = 22

    global chan
    client, chan = establish_connection(ip, port, user, password)
    
    if client:
        print("Communicating with server")
        output = send_command(chan, 'Client connected!')
        print(output)
        chan.send(getpass.getuser().encode())
        chan.send(get_mac_address().encode())
        print(chan.recv(1024).decode())


        try:
            while True:
                # chan = client.get_transport().get_channel()
                if not client.get_transport().is_active():
                    raise ServerDownError("Server is down")
                if chan.active:
                    pass
                    # data = chan.recv(1024).decode()
                    # if data :
                    #     print(data)
                    # Optionally check for data from the server
                    # data = receive_output(chan)
                    # if data:
                    #     print(data)
                else:
                    print("Channel is no longer active.")
                    break
                
        except ServerDownError as e:
            print(e)
        
        finally:
            # Ensure proper cleanup
            if client.get_transport().is_active():
                client.get_transport().close()
            if chan:
                chan.close()
            if client:
                client.close()
            print('Client disconnected...')
            firewall.flush()

if __name__ == '__main__':
    main()
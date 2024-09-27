import paramiko
import threading
import socket
import sys
import os
import paramiko.pkey
import pickle 
from concurrent import futures
import scapy.all as scapy
import firewall_server

activeThreads = 0
usableThreads = 12


client_list = []
# allowed_hosts = firewall_server.allowed_hosts
# clients = firewall_server.clients
client_objects = []
channels = []
ssh_running = True

threadpool = futures.ThreadPoolExecutor(max_workers=usableThreads)
lock = threading.Lock()

def call():
    return client_list,firewall_server.allowed_hosts,firewall_server.clients

# CWD = os.path.dirname(os.path.realpath(__file__))
hostkey = paramiko.RSAKey(filename='/home/kali/.ssh/id_rsa',password='Sudershan@98421')

def client_handler(client,session, ip):
    global activeThreads
    with lock:
        activeThreads += 1
    # print("Awaiting connection")
    
    chan = session.accept(20)
    channels.append(chan)
    client_objects.append(client)
    if chan is None:
        event.set()
        return 

    try:
        print(chan.recv(1024).decode())
        chan.send("Welcome to the session".encode())
        client_user = chan.recv(1024).decode()
        client_ip = ip
        client_mac = chan.recv(1024).decode()
        chan.send('Got your details...'.encode())
        client_list.append(dict(user_name=client_user, ip=client_ip, mac=client_mac))
        
        while True:
            # Check if the channel is still active
            if not ssh_running:
                break
            if not chan.active:
                print(f"Channel is no longer active for {ip}.")
                break
            
            try:
                buff = chan.recv(1024)
                if buff:
                    print(buff)
                    ob = pickle.loads(buff)
                    payload = ob.get('payload')
                    ip_header = scapy.IP(payload)
                    payload = payload[ip_header.ihl * 4:]
                    print(payload)
                else:
                    print(f"No data received from {ip}. Client may have disconnected.")
                    break  # Break if no data is received
            except Exception as e:
                print(f"Error while receiving data: {e}")
                break

    except Exception as e:
        print(f"Error in client handler: {e}")
    
    finally:
        print(f"Closing connection for {ip}")
        session.close()
        try:
            if chan.active:
                chan.close()
        except Exception as e:
            print(f"Error closing channel: {e}")
        
        try:
            if client in client_objects:
                client_objects.remove(client)
            if ip in firewall_server.clients:
                firewall_server.clients.remove(ip)
            # if ip in firewall_server.allowed_hosts:
            #     firewall_server.allowed_hosts.remove(ip)
            client_list[:] = [dic for dic in client_list if dic['ip'] != ip]

            # print(clients)
            # print(allowed_hosts)
            # print(client_list)
            
        except Exception as e:
            print(f"Error removing client from list: {e}")
        
        try:
            if chan in channels:
                channels.remove(chan)
        except Exception as e:
            print(f"Error removing channel from list: {e}")

        print(chan.active)
        
        with lock:
            activeThreads -= 1


# pkey = paramiko.pkey.PKey()
# hostkey = pkey.from_private_key_file(filename='~/.ssh/id_rsa')

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.completion_event = threading.Event()
    
    def check_channel_request(self,kind,chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self,username,password):
        if username == 'kali' and password == 'kali':
            print("auth success")
            return paramiko.AUTH_SUCCESSFUL
        print('Authentication failed')
        print(username)
        return paramiko.AUTH_FAILED

    def check_channel_shell_request(self,channel):
        self.completion_event.set()
        return True

def handleTerminate():
    while True:
        # print('hi')
        if not ssh_running :
            sys.exit(1)

def firewall():
    try:
        firewall_server.main()
    except Exception as e:
        print(e)
        print("Exiting")
        firewall_server.nf.unbind()
        # firewall_server.flush()

    
# eve = threading.Event()
def main():
    addr = '192.168.232.70'
    port = 22
    try:
        global activeThreads
        threadpool.submit(firewall)
        ssh_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ssh_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        ssh_server.bind((addr,port))
        ssh_server.listen(100)
        threading.Thread(target=handleTerminate).start()
        
        print("[*] Listening for connection....")
        while activeThreads <= usableThreads:
            try:
                client, addr = ssh_server.accept()
                print("[*] Got a connection from:", addr)

                # Create a new session for each connection
                session = paramiko.Transport(client)
                session.add_server_key(hostkey)
                server = Server()
                session.start_server(server=server)

                # Start a new thread to handle the client
                threadpool.submit(client_handler, client, session, addr[0])
                
            except Exception as e:
                print(f"Error accepting connection: {e}")
    except KeyboardInterrupt:
        print(e)
    # finally:
        # print("Shutting down the server....")
        # # chan.close()
        # ssh_server.close()
        # firewall_server.flush()
        # threadpool.shutdown(wait=True)
        # print(os.getpid())
        # eve.set()
        '''client,add = ssh_server.accept()
    except Exception as e:
        print("[!] Listening failed..."+str(e))
        sys.exit(1)
    else:
        print("[*] Got a Connection....Connected")
    
    bh_session = paramiko.Transport(client)
    bh_session.add_server_key(hostkey)
    server = Server()
    bh_session.start_server(server=server,event=threading.Event())

    chan = bh_session.accept(20)
    if chan is None:
        print("[!] No Channel ")
        sys.exit(1)

    command = chan.recv(1024)
    print(command.decode())
    chan.send("Welcome to bh_ssh")

    try:
        while True:
            cmd = input("Enter the command : >$ ")

            if cmd != 'exit':
                chan.send(cmd)
                print(chan.recv(10240).decode())

            else:
                chan.send('exit')
                print("Session is terminating..")
                bh_session.close()
                break
    except KeyboardInterrupt:
        bh_session.close()
        sys.exit(1)'''
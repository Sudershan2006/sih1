import shlex
import subprocess
import paramiko
import getpass
import os
import logging
import time
import firewall

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

def main():
    user = "kali"
    password = "kali"
    ip = '127.0.0.1'
    port = 22

    client,chan = establish_connection(ip, port, user, password)
    if client:
        print("Communicating with server")
        output = send_command(chan,'Client Connected!')
        print(output)
        # firewall.main()
        while(True):
            packet = firewall.pack
            # if packet:
            #     try:
            #         chan.send(packet)
            #     except Exception as e:
            #         print(e)
        
            # try:
            # except Exception as e:
            #     chan.send(e)
        # print("hi")
        client.close()

if __name__ == '__main__':
    main()
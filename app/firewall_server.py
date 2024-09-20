import subprocess
import shlex
from netfilterqueue import NetfilterQueue
import scapy.all as scapy
# import app

allowed_hosts = []
def block_all():
    args = 'sudo iptables -I INPUT -j DROP'
    args1 = 'sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT'
    args2 = 'sudo iptables -I INPUT -d 127.0.0.1 -j ACCEPT'
    args3 = 'sudo iptables -I INPUT -s 127.0.0.1 -j ACCEPT'
    # args4 = 'sudo iptables -A OUTPUT -o lo -j ACCEPT'
    try:
        # subprocess.run(shlex.split(args4),stdout=subprocess.PIPE)
        subprocess.run(shlex.split(args1),stdout=subprocess.PIPE)
        subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
        subprocess.run(shlex.split(args2),stdout=subprocess.PIPE)
        subprocess.run(shlex.split(args3),stdout=subprocess.PIPE)
        print("Connections blocked....")
    except Exception as e:
        print("[!][!] Error occurred while blocking all the packets......")

def save_rules():
    args = 'sudo iptables-save > /etc/iptables/rules.v4'
    try:
        subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
        print("Rules saved....")
    except Exception as e:
        print("[!][!] Error occurred while flushing the rules......")

def flush():
    args = 'sudo iptables -F INPUT'
    try:
        subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
        print("All the rules are flushed out....")
    except Exception as e:
        print("[!][!] Error occurred while saving the rules......")

def list():
    args = 'sudo iptables -L'
    try:
        result = subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
        print("Listing rules...")
        print(result.stdout.decode('utf-8'))
    except Exception as e:
        print("[!][!] Error occurred while listing the rules......")

def modify(ip):
    args = f'sudo iptables -A INPUT -s {ip} -p tcp --dport 22 -j ACCEPT'
    try:
        result = subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
    except Exception as e:
        print("[!][!] Error occurred while listing the rules......")
    


def process_packet(packet):
    ip  = scapy.IP(packet.get_payload())
    ether = scapy.Ether(packet.get_payload())
    if ip[scapy.IP].src not in allowed_hosts:
        print(f"Client whose ip_address : {ip[scapy.IP].src} and mac_address : {ether[scapy.Ether].src} is trying to connect...")
        if(input("Allow? (Y or N) : ")=='Y'):
            packet.accept()
            print("Packet accepted")
            # modify(ip[scapy.IP].src)
            allowed_hosts.append(ip[scapy.IP].src)
    elif(ip[scapy.IP].src in allowed_hosts):
        packet.accept()
    else:
        packet.drop()
        print("Packet dropped....")

    
    # # Parse the packet using scapy
    # scapy_packet = scapy.IP(payload)
    
    # # Access the IP header fields
    # source_ip = scapy_packet[scapy.IP].src
    # destination_ip = scapy_packet[scapy.IP].dst
    
    # # Print the IP header information
    # print(f"Source IP: {source_ip}")
    # print(f"Destination IP: {destination_ip}")
    # print("Payload: ")
    # scapy.Ether(payload).show()
    # print("\n\n")



def main():
    args = 'iptables -I INPUT -p tcp --dport 22 -j NFQUEUE --queue-num 0'
    flush()
    block_all()
    nf.bind(0,process_packet)
    try:
        result = subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
        # print(result.stdout.decode('utf-8'))
    except Exception as e:
        print("Invalid command")
    list()
    try:
        print("Waiting for packets....")
        nf.run()
    except Exception|KeyboardInterrupt:
        # flush()
        save_rules()
        raise 'Exception'
    

nf = NetfilterQueue()

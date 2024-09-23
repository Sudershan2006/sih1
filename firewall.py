import subprocess
import shlex
from netfilterqueue import NetfilterQueue
import scapy.all as scapy


def block_all():
    args = 'sudo iptables -I INPUT -j DROP'
    args1 = 'sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT'
    args2 = 'sudo iptables -A INPUT -s 127.0.0.1 -j ACCEPT'
    args3 = 'sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT'
    # args4 = 'sudo iptables -A OUTPUT -o lo -j ACCEPT'
    try:
        # subprocess.run(shlex.split(args4),stdout=subprocess.PIPE)
        subprocess.run(shlex.split(args3),stdout=subprocess.PIPE)
        subprocess.run(shlex.split(args2),stdout=subprocess.PIPE)
        subprocess.run(shlex.split(args1),stdout=subprocess.PIPE)
        subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
    except Exception as e:
        print("[!][!] Error occurred while blocking all the packets......")

def save_rules():
    args = 'sudo iptables-save > /etc/iptables/rules.v4'
    try:
        subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
    except Exception as e:
        print("[!][!] Error occurred while flushing the rules......")

def flush():
    args = 'sudo iptables -F INPUT'
    try:
        subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
    except Exception as e:
        print("[!][!] Error occurred while saving the rules......")

def list():
    args = 'sudo iptables -L'
    try:
        result = subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
    except Exception as e:
        print("[!][!] Error occurred while listing the rules......")

pack = ''

def process_packet(packet):
    pack = packet
    
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
    args = 'iptables -I INPUT -p tcp --dport 80 -j NFQUEUE --queue-num 0'
    flush()
    block_all()
    try:
        result = subprocess.run(shlex.split(args),stdout=subprocess.PIPE)
        # print(result.stdout.decode('utf-8'))
    except Exception as e:
        print("Invalid command")
    save_rules()
    list()
    

    

# try:
#     main()
# except Exception:
#     print("Exiting")
#     nf.unbind()
    

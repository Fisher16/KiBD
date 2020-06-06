from scapy.all import sniff
#This script need sudo privileges to run.
#It continously sniffs packets and prints port and initial rand seq. 

SYN_FILTER="tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & (tcp-ack) = 0"

def prt_random(pkt):
    print("{}\t{}".format(pkt[0].sport,pkt[0].seq))

sniff(filter=SYN_FILTER,store=0,prn=prt_random)

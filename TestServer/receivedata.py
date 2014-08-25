import socket, sys, struct
from time import time

# the above code breaks down the packet into IP Header + TCP Header 

def receiveData():

	# create an INET, raw socket
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

	# receive a packet
	packet = s.recvfrom(65536)
	
	#packet string from tuple
	packet = packet[0]
	
	# take first 20 characters for the ip header
	ip_header = packet[0:20]
	# header format: http://nmap.org/book/tcpip-ref.html
	
	# unpack them
	iph = struct.unpack('!2B3H2BH4s4s' , ip_header)   
	# the unpack function is used to break down the packet.
	# format characters: https://docs.python.org/2/library/struct.html#format-characters
	
	# parse IP header
	total_length = iph[2]
	protocol_number = iph[6]

	source_address = socket.inet_ntoa(iph[8]);
	destination_address = socket.inet_ntoa(iph[9]);   

	if protocol_number == 1:
		protocol_id = 'ICMP'
	elif protocol_number == 6:
		protocol_id = 'TCP'
	elif protocol_number == 17:
		protocol_id = 'UDP'

	# take first 20 characters for the tcp header
	tcp_header = packet[20:40]
	
	# unpack them
	tcph = struct.unpack('!HHLLBBHHH' , tcp_header)

	# parse TCP header
	destination_port = tcph[1]    

	# receive time
	current_time = time()

	data =  {	
		"time" : current_time,
		"protocol" : protocol_id,
		"source address" : source_address,
		"destination address" : destination_address,
		"destination port" : destination_port,
		"packet size" : total_length
		}	      

	return data

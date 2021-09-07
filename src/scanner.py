import socket, subprocess
import websocket
import logging
from scapy.all import ARP, Ether, srp

logging.getLogger('scrapy').setLevel(logging.WARNING)

def get_local_address():
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		addr = ''
		try: 
			s.connect(('10.255.255.255',1))
			addr = s.getsockname()[0]
		except:
			addr = '127.0.0.1'
		finally:
			s.close()
		return addr

def scan_network( on_device_appended=lambda device:None, on_device_failed=lambda device:None ):
	loc_addr = get_local_address()
	target_addr = loc_addr[:loc_addr.rindex('.')] + '.1/24'
	arp = ARP(pdst=target_addr)
	eth = Ether(dst='ff:ff:ff:ff:ff:ff')
	res = srp( eth/arp, timeout=3 )[0]

	servers = [ y.psrc for x,y in res ]
	
	validServers = []
	for server in servers:
		try:
			w = websocket.WebSocket()
			w.connect(f'ws://{server}:81',timeout=0.5)
			w.send('WCHATPING')
			ans = w.recv()
			if not ans == 'WCHATPONG':
				raise websocket.WebSocketBadStatusException
			validServers.append(server)
			on_device_appended(server)
		except:
			on_device_failed(server)
			pass
		finally:
			w.close()

	return {
		'found': servers,
		'valid': validServers
	}
	

	'''
	address_root = loc_addr[:loc_addr.rindex('.')]
	for v in range(0,255):
		ping_addr = address_root + '.' + str(v) #+ ':' + str(port)
		print('Scanning '+ping_addr)
		proc = subprocess.Popen( ('ping', '-c 1', '-t 0.3', ping_addr) )
		out, err = proc.communicate()
		print(proc.returncode)
	'''
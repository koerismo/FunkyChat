import socket, subprocess

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

def scan_network(port):
	loc_addr = get_local_address()
	address_root = loc_addr[:loc_addr.rindex('.')]
	for v in range(0,255):
		ping_addr = address_root + '.' + str(v) #+ ':' + str(port)
		print('Scanning '+ping_addr)
		proc = subprocess.Popen( ('ping', '-c 1', '-t 0.3', ping_addr) )
		out, err = proc.communicate()
		print(proc.returncode)

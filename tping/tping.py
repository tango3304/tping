from importlib import import_module
from string import ascii_letters
from random import choices, randint
from tchecksum import tchecksum
socket = import_module('socket')

class PingSocket:

	def __init__(self, ipaddress, timeout):
	# Check ipaddress and data StrType [ipaddressとdataが文字列型か確認]
		if (type(ipaddress) is not str):
			print(f'No Arguments IPaddress StrType [IPaddress引数が文字列型ではない]')
			return exit(1)
		if type(timeout) != int:
			print(f'No Arguments Timeout IntType [Timeout引数が整数型ではない]')
			return exit(1)
		
		self.ipaddr = ipaddress
		self.data = None
		self.timeout = timeout
		self.bufsize = 4096
		self.receive_result = None


	def ping_socket(self):
		try:
		# Add Generate data [作成したdataを追加]
		# Create IMCP Packet [ICMPパケット作成]
			self.data = PingSocket.generate_ramdom_data()
			icmp_packet = PingSocket.send_icmp_packet(self.data)

		# Destination Send ICMP Packet [宛先にICMPパケットを送信]
		# Destination Connection SendPacket And Return RecivePacket [接続できれば、パケットを送信し、受信パケットを返す]
		# Destination Not Connection Return Timeout[接続できなければ、タイムアウトを返す]
			with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as ping_socket:
				ping_socket.settimeout(self.timeout)
				ping_socket.connect((self.ipaddr,0))
				ping_socket.send(icmp_packet)
				self.receive_result = ping_socket.recv(self.bufsize)
				return self.receive_result
		except TimeoutError:
			self.receive_result = 'Timeout'
			return self.receive_result
	
	
	def generate_ramdom_data():
	# Generate data Length [dataの長さを生成]
	# Generate data Length Values [dataの長さ分の値を生成]
	# Return Value string Type [戻り値 文字列型]
		random_int = 32
		random_values = ''.join(choices(ascii_letters, k=random_int))
		return random_values
	

	def send_icmp_packet(data):
	# Initialization Variables [変数の初期化]
		"""
		Type: 08
		Code: 00
		Identifer1(id1): 00
		Identifer2(id2): 01
		Sequence1(seq1): 00
		Sequence2(seq2): random(1-10)
		Data: ArgumentValue [引数値]
		"""
		icmp_type = 0x08
		icmp_code = 0x00
		icmp_id1 = 0x00
		icmp_id2 = 0x01
		icmp_seq1 = 0x00
		icmp_seq2 = randint(0x01,0x10)

	# Calculation Checksum [チェックサムを計算]
	# Split for Packet ChecksumValue [チェックサム値をパケット用に分割]
	# tchecksum: https://github.com/tango3304/tchecksum/blob/main/tchecksum/tchecksum.py
		checksum = tchecksum.CheckSum(icmp_type, icmp_code, icmp_id1, icmp_id2, icmp_seq1, icmp_seq2, data).t_checksum()
		checksum1 = checksum >> 8
		checksum2 = ((checksum << 8) & 0xffff) >> 8

	# AddList type & code & checksum & id & seq & data [type & code & checksum & id & seq & dataをリスト追加]
	# Return Value bytes Type [戻り値 bytes]
		send_packet = [icmp_type, icmp_code, checksum1, checksum2, icmp_id1, icmp_id2, icmp_seq1, icmp_seq2]
		send_packet.extend(data.encode('UTF-8'))
		return bytes(send_packet)

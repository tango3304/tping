# tping
EchoRequest and EchoReply Module

◇Install Command [インストールコマンド]

pip install git+https://github.com/tango3304/tping.git

DependentPackage: tchecksum

https://github.com/tango3304/tchecksum

# ImportSentence [インポート文]

from tping.tping import PingSocket

# Execution [実行]

受信ICMPパケット、パケット送受信の時間 = PingSocket(対象IPアドレス, タイムアウト時間).ping_socket()

receive_icmp_result, timestamp = PingSocket(ipaddress, timeout).ping_socket()

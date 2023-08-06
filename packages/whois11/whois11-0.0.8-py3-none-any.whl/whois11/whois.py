import socket
from .whois_server import WhoisServer


MAX_BUF_LEN = 4096
PORT = 43


class Whois:

    @classmethod
    def get_whois_info(cls, domain_name, print_iana_info_flag=False):

        whois_server = WhoisServer.get_whois_server(domain_name, print_iana_info_flag)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((whois_server, PORT))
        client.send((domain_name + "\r\n").encode("utf-8"))
        
        ref = []
        while True:
            buf = client.recv(MAX_BUF_LEN)
            if buf == b'':
                break
            ref.append(buf)

        client.close()

        return b''.join(ref).decode("utf-8")

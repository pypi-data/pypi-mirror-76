import socket
import ssl
from . import errors


MAX_BUF_LEN = 4096

HOST = "www.iana.org"
PORT = 443
QUERY = "/whois?q="
USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko"


class WhoisServer:

    @classmethod
    def get_whois_server(cls, domain_name, print_iana_info_flag=False):

        query = QUERY + domain_name
        req = ("GET {0} HTTP/1.1\r\n"
               "Host: {1}\r\n"
               "User-Agent: {2}\r\n"
               "Connection: close\r\n"
               "\r\n")
        req = req.format(query, HOST, USER_AGENT).encode("utf-8")

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client = ssl.wrap_socket(client,
                                 keyfile=None,
                                 certfile=None,
                                 server_side=False,
                                 cert_reqs=ssl.CERT_NONE,
                                 ssl_version=ssl.PROTOCOL_SSLv23)
        client.sendall(req)

        res = []
        while True:
            buf = client.recv(MAX_BUF_LEN)
            if buf == b'':
                break
            res.append(buf)

        client.close()

        s = b''.join(res).decode("utf-8")
        s = s.split("\n")

        if len(s) >= 0:
            if s[0].find(" 200 OK") == -1:
                raise errors.WhoisError("could not get whois server: [HTTP error]")

        if print_iana_info_flag:
            print_flag = False
            for x in s:
                if x.find("</pre>") >= 0:
                    print_flag = False
                if print_flag:
                    print(x)
                if x.find("<pre>") >= 0:
                    print_flag = True
                    print(x[x.find("<pre>") + 5:])

        for x in s:
            if x.find("whois:") != -1:
                x = x.split(" ")
                if len(x) >= 2:
                    return x[-1]

        raise errors.WhoisError("could not get whois server: [whois server parse error]")

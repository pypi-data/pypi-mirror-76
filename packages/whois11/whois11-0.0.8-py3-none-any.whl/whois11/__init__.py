from .whois import Whois
from .errors import WhoisError


def whois(domain_name, print_iana_info_flag=False):
    return Whois.get_whois_info(domain_name, print_iana_info_flag)

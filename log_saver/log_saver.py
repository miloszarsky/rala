import os
import time
import redis
import uuid
import ipaddress
from netaddr import *

def is_valid_ipv4(ip4):
    try:
        ipaddress.IPv4Address(ip4)
        return True
    except ipaddress.AddressValueError:
        return False

def is_valid_ipv6(ip6):
    try:
        ipaddress.IPv6Address(ip6)
        return True
    except ipaddress.AddressValueError:
        return False

ip_ttl = os.getenv('IP_TTL')

r = redis.Redis(host='rala-redis', port=6379, decode_responses=True)
f = open('/file.log', 'r+')
f.truncate(0) # need '0' when using r+

while True:
    line = ''
    while len(line) == 0 or line[-1] != '\n':
        tail = f.readline()
        if tail == '':
            time.sleep(0.1)          # avoid busy waiting
            # f.seek(0, io.SEEK_CUR) # appears to be unneccessary
            continue
        line+=tail
    #print(line)
    rawline = line.strip()
    parser = rawline.split(" ")
    #reverse to remove port
    iprev = parser[5][::-1]
    #split by :
    ipremoveport = iprev.split(":",1)
    #get all after :
    iprawrev = ipremoveport[1]
    #reverse back to original
    ipraw = iprawrev[::-1]
    #print(ipraw)
    if is_valid_ipv4(ipraw):
        r.set('ip4-'+str(uuid.uuid4()), ipraw, ex=ip_ttl)
    if is_valid_ipv6(ipraw):
        r.set('ip6-'+str(uuid.uuid4()), ipraw, ex=ip_ttl)

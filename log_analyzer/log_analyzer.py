import os
import time
import redis
from collections import Counter
from itertools import takewhile, dropwhile
import smtplib
from email.mime.text import MIMEText
import paramiko
import http.client, urllib

r = redis.Redis(host='rala-redis', port=6379, decode_responses=True)

# Mail Configuration
mailing = os.getenv('MAILING')
port = os.getenv('MAIL_PORT')
smtp_server = os.getenv('MAIL_SERVER')
login = os.getenv('MAIL_LOGIN')
password = os.getenv('MAIL_PASSWORD')
sender_email = os.getenv('MAIL_SENDER')
receiver_email = os.getenv('MAIL_RECIPIENT')

# SSH Configuration
ssh_host = os.getenv('SSH_HOST')
ssh_port = os.getenv('SSH_PORT')
ssh_username = os.getenv('SSH_USERNAME')
ssh_password = os.getenv('SSH_PASSWORD')
ssh4_cmd1 = os.getenv('SSH4_CMD1')
ssh4_cmd2 = os.getenv('SSH4_CMD2')
ssh6_cmd1 = os.getenv('SSH6_CMD1')
ssh6_cmd2 = os.getenv('SSH6_CMD2')

# PUSHOVER Configuration
pushover = os.getenv('PUSHOVER')
pushover_user = os.getenv('PUSHOVER_USER')
pushover_token = os.getenv('PUSHOVER_TOKEN')

# ENV
ip_count_threshold = os.getenv('IP_COUNT_THRESHOLD')

#function actions
def mailer (addrs):
    message = MIMEText(str(addrs), "plain")
    message["Subject"] = "Rala"
    message["From"] = sender_email
    message["To"] = receiver_email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def ssh4 (addrs4):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_host, username=ssh_username, password=ssh_password, port=ssh_port)
    _stdin, _stdout,_stderr = client.exec_command(str(ssh4_cmd1) + str(addrs4) + str(ssh4_cmd2))
    client.close()

def ssh6 (addrs6):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ssh_host, username=ssh_username, password=ssh_password, port=ssh_port)
    _stdin, _stdout,_stderr = client.exec_command(str(ssh6_cmd1) + str(addrs6) + str(ssh6_cmd2))
    client.close()

def pushoversender(address):
    data={"token": pushover_token,"user": pushover_user,"message": str(address),}
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json", urllib.parse.urlencode(data), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

while True:
    ips4=[]
    ips6=[]
    for ip4 in Counter(r.keys(pattern='ip4-*')):
        #print(r.get(ip4))
        ips4.append(r.get(ip4))
    #print(collections.Counter(ips4))
    higher4 = dict(takewhile(lambda i: i[1] > int(ip_count_threshold), Counter(ips4).most_common()))
    if not higher4:
        print("NoValues4 in threshold")
    else:
        for addrs4, counter in higher4.items():
            #whatever you want to do with ip in key
            print(addrs4)
            if mailing == "true":
                mailer(addrs4)
            if pushover == "true":
                pushoversender(addrs4)
            ssh4(addrs4)
    for ip6 in Counter(r.keys(pattern='ip6-*')):
        #print(r.get(ip6))
        ips6.append(r.get(ip6))
    #print(collections.Counter(ips6))
    higher6 = dict(takewhile(lambda i: i[1] > int(ip_count_threshold), Counter(ips6).most_common()))
    if not higher6:
        print("NoValues6 in threshold")
    else:
        for addrs6, counter in higher6.items():
            #whatever you want to do with ip in key
            print(addrs6)
            if mailing == "true":
                mailer(addrs6)
            if pushover == "true":
                pushoversender(addrs6)
            ssh6(addrs6)
    time.sleep(5)

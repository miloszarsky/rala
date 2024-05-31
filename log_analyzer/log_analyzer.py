import os
import time
import redis
from collections import Counter
from itertools import takewhile, dropwhile
import smtplib
from email.mime.text import MIMEText
import paramiko

r = redis.Redis(host='rala-redis', port=6379, decode_responses=True)

# Mail Configuration
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
ssh_command1 = os.getenv('SSH_CMD1')
ssh_command2 = os.getenv('SSH_CMD2')

# ENV
ip_count_threshold = os.getenv('IP_COUNT_THRESHOLD')

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
            ###
            #email result
            #message = MIMEText(str(addrs4), "plain")
            #message["Subject"] = "Rala"
            #message["From"] = sender_email
            #message["To"] = receiver_email
            #with smtplib.SMTP(smtp_server, port) as server:
            #    server.starttls()
            #    server.login(login, password)
            #    server.sendmail(sender_email, receiver_email, message.as_string())
            ###
            #run action over ssh
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ssh_host, username=ssh_username, password=ssh_password, port=ssh_port)
            _stdin, _stdout,_stderr = client.exec_command(str(ssh_command1) + str(addrs4) + str(ssh_command2))
            client.close()
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
            ###
            #email result
            #message = MIMEText(str(addrs6), "plain")
            #message["Subject"] = "Rala"
            #message["From"] = sender_email
            #message["To"] = receiver_email
            #with smtplib.SMTP(smtp_server, port) as server:
            #    server.starttls()
            #    server.login(login, password)
            #    server.sendmail(sender_email, receiver_email, message.as_string())
            ###
            #run action over ssh
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ssh_host, username=ssh_username, password=ssh_password, port=ssh_port)
            _stdin, _stdout,_stderr = client.exec_command(str(ssh_command1) + str(addrs6) + str(ssh_command2))
            client.close()
    time.sleep(5)

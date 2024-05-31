# rala
**Realtime Access Log Analyzer**

*Based on docker, python, redis.*

## Main goal:
 * To analyze access log as quick as possible and run action if something wrong was identified (eg. ban ip in firewall).
 * Create first/second line of defense against bad bots, ddos ​​app attacks and others
   
### Implemented:
 * haproxy log defaults
   
### ToDo:
 * apache log defaults
 * nginx log defaults
 * customize log parser
 * remote input (rsyslog)

## How it works:
 * writes lines from log to redis to ipv4 and ipv6 keys
 * counts ipv4 and ipv6 arrays and give ip above threshold as output
 * runs actions on output values

## Howto:
 * edit .env according your needs
 * edit docker-compose.yml and mount your log file
 * optionaly uncomment mail functions in analyzer python
 * cmd variables in env works as CMD1 + \<OUTPUT VALUE\> + CMD2
 
First code release planned to 1.6.2024


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/miloszarsky)

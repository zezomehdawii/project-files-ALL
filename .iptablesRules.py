import os

eth="eth0"
wlan="wlan0"
with open("ip_list.txt","r") as fr:
    iplist = fr.read()
    print (iplist)
    os.system("sudo iptables -F")
    os.system("sudo iptables -t nat -F")
    os.system(f"sudo iptables -t nat -A POSTROUTING -o {eth} -j MASQUERADE")
    os.system(f"sudo iptables -t nat -A PREROUTING -d {iplist} -j NFQUEUE --queue-num 1")
    os.system(f"sudo iptables -A FORWARD -i {eth} -o {wlan} -m state --state RELATED,ESTABLISHED -j ACCEPT")
    os.system(f"sudo iptables -A FORWARD -i {wlan} -o {eth} -j ACCEPT")

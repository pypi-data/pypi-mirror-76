from scapy.all import *
import threading
import argparse
import logging
import re

from scapy.layers.l2 import ARP

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

def parse_ip(targets):
    '''
    解析192.168.1.1-254整个网段形式的IP段，分解成IP列表
    '''
    _split = targets.split('-')
    first_ip = _split[0]
    ip_split = first_ip.split('.')
    ipdot4 = range(int(ip_split[3]),int(_split[1])+1)
    ipaddrs = [ip_split[0]+'.'+ip_split[1]+'.'+ip_split[2]+'.'+str(p) for p in ipdot4]
    return ipaddrs

def arp_scan(target_ip):
    '''
    ͨ通过scapy的sr1函数进行ARP扫描
    '''
    try:
        ans = sr1(ARP(pdst=target_ip),timeout=1,verbose=False)
        if ans:
            return ans
    except Exception:
        print('[-]发包错误')
        exit(1)

def parse_arp(target_ip):
    '''
    解析收到的ARP reply包，采集IP及其对应的MAC
    '''
    ans = arp_scan(target_ip)
    if ans:
        if ans.haslayer('ARP') and ans.fields['op'] == 2:
            print('[+] IP:%s => MAC:%s' % (ans.fields['psrc'],ans.fields['hwsrc']))

if __name__ == '__main__':
    usage = 'python %(prog)s -t [targets]'
    parser = argparse.ArgumentParser(usage=usage,epilog='以上做为说明，祝好运！',description='说明：指定IP或IP段进行ARP扫描.')
    parser.add_argument('-t',action='store',dest='targets',help='targets为IP或IP段，如192.168.1.x或192.168.1.1-254')

    args = parser.parse_args()
    if args.targets == None:
        parser.print_help()
    elif (not re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',args.targets)) and \
            (not re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}$',args.targets)):
        parser.print_help()
    else:
        targets = args.targets


    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',targets):
        ip = targets
        parse_arp(ip)
    elif re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}-\d{1,3}$',targets):
        ips = parse_ip(targets)
        for ip in ips:
            t = threading.Thread(target=parse_arp,args=(ip,))
            t.start()

#!/usr/bin/python3
import requests
import re
import sys
import argparse
from subprocess import Popen, PIPE

cmd = 'ss -tap'
exclude_values = [None, '127.0.0.1', '0.0.0.0']


def getLastIpaddressesInLine(string_with_addr):
    ipList = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', string_with_addr)
    if len(ipList):
        return ipList[-1]
    return None


def takeSecond(elem):
    return elem[1]


def callCommand():
    process = Popen(cmd, stdout=PIPE, shell=True)
    output = process.communicate()[0].decode('utf-8')
    return output.split('\n')


def whois(idaddr, param='isp'):
    url = f"http://demo.ip-api.com/json/{idaddr}"
    response = requests.request("GET", url)
    data = response.json()
    return data.get(param)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Whois param script",
                                     usage="Get current most usable ip addresses and information about ip owner from "
                                           "ip-api.com")
    parser.add_argument('-p', '--proc', help=' Filter output my PID or process name', type=str, default='')
    parser.add_argument('-l', '--lines', help=' Limit output lines ', type=int, default=0)
    parser.add_argument('-w', '--who', help=' Change whois attribute name (default key = "isp")', type=str,
                        default='isp')
    parser.add_argument('-s', '--state', help=' Filter output by TCP state ', type=str, default='')
    args = parser.parse_args()
    lines =  callCommand()
    if not args.proc:
        lines = [line for line in lines if line.find(f'users:(("{args.proc}"') >= 0 or line.find(f'pid={args.proc},') >= 0]
    if not args.state:
        lines = [line for line in lines if re.split('\s+', line)[0].find(args.state) >= 0]

    targetip_list = [ ip for ip in [ getLastIpaddressesInLine(line) for line in lines] if ip not in exclude_values]
    cnt_list = [[ind, targetip_list.count(ind)] for ind in set(targetip_list)]
    cnt_list.sort(key=takeSecond, reverse=True)
    if 0 < args.lines < len(cnt_list):
        cnt_list = cnt_list[:args.lines]
    print(f"Address\t\t\tConn numbers\tKey '{args.who}' Value")
    print("===================================================")
    for ip_cnt in cnt_list:
        ip_cnt.append(whois(ip_cnt[0], args.who))
        print(f"{ip_cnt[0]}\t\t{ip_cnt[1]}\t\t{ip_cnt[2]}")
    print("===================================================")

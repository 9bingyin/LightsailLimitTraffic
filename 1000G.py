#!/usr/bin/python
#coding=utf-8
import sys,re,time,os
maxdata = 1073741824000 #流量上限，包括流入和流出，单位Byte
memfilename = '/root/newnetcardtransdata.txt'
netcard = '/proc/net/dev'
def checkfile(filename):
    if os.path.isfile(filename):
        pass
    else:
        f = open(filename, 'w')
        f.write('0')
        f.close()
def get_net_data():
    nc = netcard or '/proc/net/dev'
    fd = open(nc, "r")
    netcardstatus = False
    for line in fd.readlines():
        if line.find("eth0") > 0:
            netcardstatus = True
            field = line.split()
            recv = field[0].split(":")[1]
            recv = recv or field[1]
            send = field[9] #如果流量计算错误，请根据/proc/net/dev的内容修改此变量
    if not netcardstatus:
        fd.close()
        print 'Please setup your netcard'
        sys.exit()
    fd.close()
    return (float(recv), float(send))
    
def net_loop():
    (recv, send) = get_net_data()
    checkfile(memfilename)
    lasttransdaraopen = open(memfilename,'r')
    lasttransdata = lasttransdaraopen.readline()
    lasttransdaraopen.close()
    totaltrans = int(lasttransdata) or 0
    while True:
        time.sleep(3)
        nowtime = time.strftime('%d %H:%M',time.localtime(time.time()))
        sec = time.localtime().tm_sec
        if nowtime == '01 00:00': #流量更新时间，默认为每月1日00:00
            if sec < 10:
                totaltrans = 0
        (new_recv, new_send) = get_net_data()
        recvdata = new_recv - recv
        recv = new_recv
        senddata = new_send - send
        send = new_send
        totaltrans += int(recvdata)
        totaltrans += int(senddata)
        memw = open(memfilename,'w')
        memw.write(str(totaltrans))
        memw.close()
        if totaltrans >= maxdata:
            os.system('rm -f /root/newnetcardtransdata.txt && init 0') #可以修改为其他命令
if __name__ == "__main__":
    net_loop()
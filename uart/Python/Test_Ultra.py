# encoding=utf-8

import serial
import time
import string
import binascii
import numpy as np

class Ultra(object):
    '''
    接口名称，波特率(器件默认为115200)
    '''
    def __init__(self,name="/dev/ttyUSB0",baud=115200):
        self.name = name
        self.baud = baud
        self.isopen = self.connect()
        self.data = ''
        self.distance = np.zeros(5)
    '''
    连接串口
    '''
    def connect(self):
        self.serial = serial.Serial(self.name,self.baud)
        if not self.serial.isOpen():
            print "Can not open serial port!"
            return False
        return True

    def recv_data(self):
        self.data = ''
        while True:
            if ord(self.serial.read(1))==0xFF:
                if ord(self.serial.read(1)) ==0xFE:
                    if ord(self.serial.read(1))==0x75:
                        self.data = self.serial.read(11)
            if len(self.data):
                break

    def checkdata(self):
        for i in self.data:
            print('%#x'%ord(i)),
        print ""

        if(ord(self.data[10]) != (ord(self.data[0])^ord(self.data[1])^ord(self.data[2])^ord(self.data[3])^ord(self.data[4])^ord(self.data[5])^ord(self.data[6])^ord(self.data[7])^ord(self.data[8])^ord(self.data[9]))):
            return 0
        else:
            return 1

    def get_distance(self):
        self.recv_data()
        if(self.checkdata()==0):
            self.distance[0] = 0.
            self.distance[1] = 0.
            self.distance[2] = 0.
            self.distance[3] = 0.
            self.distance[4] = 0.
        else:
            self.distance[0] =float(ord(self.data[0])<<8|ord(self.data[1]))/1000.
            self.distance[1] =float(ord(self.data[2])<<8|ord(self.data[3]))/1000.
            self.distance[2] =float(ord(self.data[4])<<8|ord(self.data[5]))/1000.
            self.distance[3] =float(ord(self.data[6])<<8|ord(self.data[7]))/1000.
            self.distance[4] =float(ord(self.data[8])<<8|ord(self.data[9]))/1000.
        return self.distance

    '''
    关闭串口
    '''
    def close(self):
        self.serial.close()

def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

'''
测试程序
'''
if __name__ == "__main__":
    try:
        myserial = Ultra("/dev/ttyUSB0",230400)
	print "Ulrea_Test"
        while True:
            print 

            myserial.serial.write(b'\xff\xfe\x75')

            nbflag = myserial.serial.in_waiting

            if nbflag:
                distance = myserial.get_distance()
                print get_time_stamp(),":",
                print "L  = ",distance[0],"  ",
                print "FL = ",distance[1],"  ",
                print "FC = ",distance[2],"  ",
                print "FR = ",distance[3],"  ",
                print "R  = ",distance[4]

            time.sleep(0.1)

    except KeyboardInterrupt:
            myserial.close()

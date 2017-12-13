# _*_ coding:utf-8 _*_

import socket
import threading
import sys
import os
import base64
import hashlib
import struct
import re
import subprocess

# ====== config ======
HOST = 'localhost'
PORT = 11528
MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HANDSHAKE_STRING = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection: Upgrade\r\n" \
                   "Sec-WebSocket-Accept: {1}\r\n" \
                   "WebSocket-Location: ws://{2}/chat\r\n" \
                   "WebSocket-Protocol:chat\r\n\r\n"


# Communication protocol
#     command:[Action]->[system command]
#         open: open the file with system command
#         other: not be handled temporary
#
#     e.g "command:open->gedit /home/qinsw/pengtian/shell/test.sh<-"


class Th(threading.Thread):
    def __init__(self, connection, address):
        threading.Thread.__init__(self)
        self.con = connection
        self.addr = address

    def run(self):
        raw_data = False
        while not raw_data:
            try:
                raw_data = self.recv_data(1024)
                print raw_data
                match = re.match(r'^command:(.+?)->(.+?)<-$', raw_data)
                if match:
                    print match.group(1), match.group(2)
                    action = match.group(1)
                    sys_command = match.group(2).decode('utf-8')
                    print sys_command
                    if action == 'open':
                        subprocess.Popen(sys_command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    else:
                        print "Not handled action : ", action
                    self.con.close()
            except Exception as e:
                print "Error message : ", e.message, "\nThere is a error in thread which contains socket from ", self.addr
        self.con.close()

    def recv_data(self, num):
        try:
            all_data = self.con.recv(num)
            if not len(all_data):
                print "no data"
                return False
        except:
            return False
        else:
            code_len = ord(all_data[1]) & 127
            if code_len == 126:
                masks = all_data[4:8]
                data = all_data[8:]
            elif code_len == 127:
                masks = all_data[10:14]
                data = all_data[14:]
            else:
                masks = all_data[2:6]
                data = all_data[6:]
            raw_str = ""
            i = 0
            for d in data:
                raw_str += chr(ord(d) ^ ord(masks[i % 4]))
                i += 1
            return raw_str

    # send data
    def send_data(self, data):
        if data:
            data = str(data)
        else:
            return False
        token = "\x81"
        length = len(data)
        if length < 126:
            token += struct.pack("B", length)
        elif length <= 0xFFFF:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)
        # struct为Python中处理二进制数的模块，二进制流为C，或网络流的形式。
        data = '%s%s' % (token, data)
        self.con.send(data)
        return True


# handshake
def handshake(con):
    headers = {}
    shake = con.recv(1024)
    if not len(shake):
        return False
    header, data = shake.split('\r\n\r\n', 1)
    for line in header.split('\r\n')[1:]:
        key, val = line.split(': ', 1)
        headers[key] = val

    if 'Sec-WebSocket-Key' not in headers:
        print ('This socket is not websocket, client close.')
        con.close()
        return False

    sec_key = headers['Sec-WebSocket-Key']
    res_key = base64.b64encode(hashlib.sha1(sec_key + MAGIC_STRING).digest())

    str_handshake = HANDSHAKE_STRING.replace('{1}', res_key).replace('{2}', HOST + ':' + str(PORT))
    print str_handshake
    con.send(str_handshake)
    return True


# Server State
__ServerRunning = False
__ServerStartListener = []
__ServerStopListener = []
__ServerSock = None
__STOP_REASON__ = {
    0x01: "Server is running, try stop server first",
    0x02: "{0} port is in use, please try start later".format(PORT),
    0x03: "Close the python web server normally"
}

"""
start a service socket and listen
when coms a connection, start a new thread to handle it
"""


def startServer():
    global __ServerRunning, __ServerConnections, __ServerSock

    if __ServerRunning:
        notifyServerStopped(0x01)
        return False

    __ServerRunning = False
    __ServerSock = None

    __ServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        __ServerSock.bind((HOST, PORT))
        # 链接队列大小
        __ServerSock.listen(1000)
        print "bind %s,ready to use" % str(PORT)
    except:
        notifyServerStopped(0x02)
        return False
        # sys.exit()

    __ServerRunning = True
    notifyServerStarted()

    while __ServerRunning:
        # 返回元组（socket,add），accept调用时会进入waited状态
        connection, address = __ServerSock.accept()

        print "Got connection from ", address

        if handshake(connection):
            print "handshake success"
            try:
                t = Th(connection, address)
                t.start()
                print 'new thread for client ...'
            except:
                print 'start new thread error'
                connection.close()
    else:
        print "__ServerRunning = False"
        __ServerRunning = False


def stopServer():
    global __ServerRunning, __ServerSock

    __ServerRunning = False
    if type(__ServerSock) is 'SocketType' and __ServerSock:
        __ServerSock.close()

    notifyServerStopped(0x03)
    __cleanServerListener()


def addServerStartListener(callback):
    global __ServerStartListener
    __ServerStartListener.append(callback)


def addServerStopedListener(callback):
    global __ServerStopListener
    __ServerStopListener.append(callback)


def notifyServerStarted():
    global __ServerStartListener
    for listener in __ServerStartListener:
        listener()


def notifyServerStopped(reason):
    global __ServerStopListener
    for listener in __ServerStopListener:
        listener(reason)


def __cleanServerListener():
    global __ServerStopListener, __ServerStartListener
    __ServerStopListener = []
    __ServerStartListener = []

    # if __name__ == '__main__':
    #    startServer()

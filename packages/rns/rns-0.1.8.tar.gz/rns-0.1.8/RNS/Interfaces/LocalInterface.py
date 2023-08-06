from .Interface import Interface
import socketserver
import threading
import socket
import time
import sys
import os
import RNS

class HDLC():
    FLAG              = 0x7E
    ESC               = 0x7D
    ESC_MASK          = 0x20

    @staticmethod
    def escape(data):
        data = data.replace(bytes([HDLC.ESC]), bytes([HDLC.ESC, HDLC.ESC^HDLC.ESC_MASK]))
        data = data.replace(bytes([HDLC.FLAG]), bytes([HDLC.ESC, HDLC.FLAG^HDLC.ESC_MASK]))
        return data

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class LocalClientInterface(Interface):

    def __init__(self, owner, name, target_port = None, connected_socket=None):
        self.IN               = True
        self.OUT              = False
        self.socket           = None
        self.parent_interface = None
        self.name             = name

        if connected_socket != None:
            self.receives    = True
            self.target_ip   = None
            self.target_port = None
            self.socket      = connected_socket

        elif target_port != None:
            self.receives    = True
            self.target_ip   = "127.0.0.1"
            self.target_port = target_port

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.target_ip, self.target_port))

            self.is_connected_to_shared_instance = True

        self.owner   = owner
        self.online  = True
        self.writing = False

        if connected_socket == None:
            thread = threading.Thread(target=self.read_loop)
            thread.setDaemon(True)
            thread.start()

    def processIncoming(self, data):
        self.owner.inbound(data, self)

    def processOutgoing(self, data):
        if self.online:
            while self.writing:
                time.sleep(0.01)

            try:
                self.writing = True
                data = bytes([HDLC.FLAG])+HDLC.escape(data)+bytes([HDLC.FLAG])
                self.socket.sendall(data)
                self.writing = False
            except Exception as e:
                RNS.log("Exception occurred while transmitting via "+str(self)+", tearing down interface", RNS.LOG_ERROR)
                RNS.log("The contained exception was: "+str(e), RNS.LOG_ERROR)
                self.teardown()


    def read_loop(self):
        try:
            in_frame = False
            escape = False
            data_buffer = b""

            while True:
                data_in = self.socket.recv(4096)
                if len(data_in) > 0:
                    pointer = 0
                    while pointer < len(data_in):
                        byte = data_in[pointer]
                        pointer += 1
                        if (in_frame and byte == HDLC.FLAG):
                            in_frame = False
                            self.processIncoming(data_buffer)
                        elif (byte == HDLC.FLAG):
                            in_frame = True
                            data_buffer = b""
                        elif (in_frame and len(data_buffer) < RNS.Reticulum.MTU):
                            if (byte == HDLC.ESC):
                                escape = True
                            else:
                                if (escape):
                                    if (byte == HDLC.FLAG ^ HDLC.ESC_MASK):
                                        byte = HDLC.FLAG
                                    if (byte == HDLC.ESC  ^ HDLC.ESC_MASK):
                                        byte = HDLC.ESC
                                    escape = False
                                data_buffer = data_buffer+bytes([byte])
                else:
                    RNS.log("Socket for "+str(self)+" was closed, tearing down interface", RNS.LOG_VERBOSE)
                    self.teardown()
                    break

                
        except Exception as e:
            self.online = False
            RNS.log("An interface error occurred, the contained exception was: "+str(e), RNS.LOG_ERROR)
            RNS.log("Tearing down "+str(self), RNS.LOG_ERROR)
            self.teardown()

    def teardown(self):
        self.online = False
        self.OUT = False
        self.IN = False

        if self in RNS.Transport.interfaces:
            RNS.Transport.interfaces.remove(self)

        if self in RNS.Transport.local_client_interfaces:
            RNS.Transport.local_client_interfaces.remove(self)


    def __str__(self):
        return "LocalInterface["+str(self.target_port)+"]"


class LocalServerInterface(Interface):

    def __init__(self, owner, bindport=None):
        self.IN  = True
        self.OUT = False
        self.name = "Reticulum"

        if (bindport != None):
            self.receives = True
            self.bind_ip = "127.0.0.1"
            self.bind_port = bindport

            def handlerFactory(callback):
                def createHandler(*args, **keys):
                    return LocalInterfaceHandler(callback, *args, **keys)
                return createHandler

            self.owner = owner
            self.is_local_shared_instance = True

            address = (self.bind_ip, self.bind_port)
            self.server = ThreadingTCPServer(address, handlerFactory(self.incoming_connection))

            thread = threading.Thread(target=self.server.serve_forever)
            thread.setDaemon(True)
            thread.start()


    def incoming_connection(self, handler):
        interface_name = str(str(handler.client_address[1]))
        spawned_interface = LocalClientInterface(self.owner, name=interface_name, connected_socket=handler.request)
        spawned_interface.OUT = self.OUT
        spawned_interface.IN  = self.IN
        spawned_interface.target_ip = handler.client_address[0]
        spawned_interface.target_port = str(handler.client_address[1])
        spawned_interface.parent_interface = self
        RNS.log("Accepting new connection to shared instance: "+str(spawned_interface), RNS.LOG_VERBOSE)
        RNS.Transport.interfaces.append(spawned_interface)
        RNS.Transport.local_client_interfaces.append(spawned_interface)
        spawned_interface.read_loop()

    def processOutgoing(self, data):
        pass

    def __str__(self):
        return "Shared Instance ["+str(self.bind_port)+"]"

class LocalInterfaceHandler(socketserver.BaseRequestHandler):
    def __init__(self, callback, *args, **keys):
        self.callback = callback
        socketserver.BaseRequestHandler.__init__(self, *args, **keys)

    def handle(self):
        self.callback(handler=self)
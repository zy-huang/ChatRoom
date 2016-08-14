# -*- coding:utf-8 -*-
import socket
import select
import sys

class CClient(object):
	"客户端socket类"
	RECV_BUFFER = 4096
	def __init__(self,sAddr,sPort):
		self.m_pSock = None
		self.m_lReadSock = [sys.stdin,]

		self.InitSock(sAddr,sPort)

	def Prompt(self):
		sys.stdout.write("<You>")
		sys.stdout.flush()

	def InitSock(self,sAddr,sPort):
		self.m_pSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.m_pSock.settimeout(2)

		self.m_pSock.connect((sAddr,sPort))
		self.m_lReadSock.append(self.m_pSock)

	def Work(self):
		while 1:
			lReadSock , lWriteSock , lErrorSock = select.select(self.m_lReadSock,[],[])
			for sock in lReadSock: 
				if sock == sys.stdin:
					sMessage = sys.stdin.readline()

					self.m_pSock.send(sMessage)
					self.Prompt()
				else:
					sMessage = self.m_pSock.recv(self.RECV_BUFFER)
					if sMessage:
						sys.stdout.write(sMessage)

					else:
						self.m_pSock.close()
						print "Disconnected from the server."
						sys.exit()


def main():
	if len(sys.argv) != 3:
		print "Usage: client.py address port"
	else:
		sAddr = sys.argv[1]
		sPort = int(sys.argv[2])

		pClient = CClient(sAddr,sPort)
		pClient.Work()

if __name__ == "__main__":
	main()
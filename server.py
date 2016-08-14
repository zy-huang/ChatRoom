# -*- coding:utf-8 -*-
import socket
import select

class CServer(object):
	"""用于监听的服务器套接字"""
	RECV_BUFFER = 4096
	def __init__(self):
		self.m_pServerSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.m_lReadSock = []
		self.m_lWriteSock = []
		self.m_lErrorSock = []
		self.m_lSockToDel = []

	#@sPort:绑定的端口号
	def Start(self,sPort):
		self.m_pServerSock.bind(("127.0.0.1",sPort))
		self.m_pServerSock.listen(5)
		self.AddReadSock(self.m_pServerSock)



	def AddReadSock(self,pReadSock):
		self.m_lReadSock.append(pReadSock)

	def RemoveReadSock(self,pReadSock):
		self.m_lReadSock.remove(pReadSock)

	def AddClocsedSock(self,pSock):
		self.m_lSockToDel.append(pSock)

	def RemoveClosedSock(self):
		for sock in self.m_lSockToDel:
			self.m_lReadSock.remove(sock)
		self.m_lSockToDel = []

	def IsClosed(self,pSock):
		if pSock in self.m_lSockToDel:
			return True
		else:
			return False

	def BroadcastData(self,pSock,sData):
		for sock in self.m_lReadSock:
			if sock != self.m_pServerSock and sock != pSock and not self.IsClosed(sock):
				try:
					sock.send(sData)
				except:
					sock.close()
					self.AddClocsedSock(sock)
		#self.RemoveClosedSock()

	def Work(self):

		while 1:
			lReadSock , lWriteSock , lErrorSock = select.select(self.m_lReadSock,self.m_lWriteSock,self.m_lErrorSock)
			
			for sock in lReadSock:
				if sock == self.m_pServerSock:
					pClientSock,vAddr = sock.accept()
					self.AddReadSock(pClientSock)

					print "Client (%s,%s) connected"%vAddr

					sMessage = "(%s,%s) entered the room\n"%vAddr
					self.BroadcastData(pClientSock,sMessage)

				else:
					try:
						sData = sock.recv(self.RECV_BUFFER)
						sMessage = "<"+str(sock.getpeername())+">:"+sData
						self.BroadcastData(sock,sMessage)
					except:

						sMessage = str(sock.getpeername())+" leaved the room\n"
						self.BroadcastData(sock,sMessage)
						sock.close()
						self.AddClocsedSock(sock)
			self.RemoveClosedSock()

def main():
	pServer = CServer()
	pServer.Start(4096)

	pServer.Work()

if __name__ == "__main__":
	main()





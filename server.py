import socketserver
import threading
import pickle
import sys

import blockchain

HOST = ''
PORT = 9009
lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성

class UserManager: # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
                   # ① 채팅 서버로 입장한 사용자의 등록
                   # ② 채팅을 종료하는 사용자의 퇴장 관리
                   # ③ 사용자가 입장하고 퇴장하는 관리
                   # ④ 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송

   def __init__(self):
      self.users = {} # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

   def addUser(self, username, conn, addr): # 사용자 ID를 self.users에 추가하는 함수
      if username in self.users: # 이미 등록된 사용자라면
         conn.send('이미 등록된 노드입니다.\n'.encode())
         return None

      # 새로운 사용자를 등록함
      lock.acquire() # 스레드 동기화를 막기위한 락
      self.users[username] = (conn, addr)
      lock.release() # 업데이트 후 락 해제

      self.sendMessageToAll('[%s]님이 입장했습니다.' %username)
      print('+++ 노드 참여자 수 [%d]' %len(self.users))

      return username

   def removeUser(self, username): #사용자를 제거하는 함수
      if username not in self.users:
         return

      lock.acquire()
      del self.users[username]
      lock.release()

      self.sendMessageToAll('[%s]님이 퇴장했습니다.' %username)
      print('--- 노드 참여자 수 [%d]' %len(self.users))


   def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
      if msg == '/quit': # 보낸 메세지가 'quit'이면
         self.removeUser(username)
         return -1

      else:
         self.sendMessageToAll('[%s] %s' %(username,msg))
         return


   def sendMessageToAll(self, msg):
      for conn, addr in self.users.values():
             conn.send(msg.encode())




class MyTcpHandler(socketserver.BaseRequestHandler):
   userman = UserManager()

   def handle(self):
      print('[%s] 연결됨' %self.client_address[0])   # 클라이언트가 접속시 클라이언트 주소 출력

      try:
          username = self.registerUsername()

          while True:
             pre_msg = self.request.recv(16394)

             #if type(pre_msg) == bytes:
             msg = pickle.loads(pre_msg)
             while pre_msg:
                 print(msg)
                 if self.userman.messageHandler(username,msg) == -1:
                     self.request.close()
                     break
                 pre_msg = self.request.recv(1024)
                 msg = pickle.loads(pre_msg)

         #else:
        #     while pre_msg:
        #         if pre_msg == 'mine'.decode():
        #             print('mining'.encode())
        #             print(pre_msg.decode())
        #             if self.userman.messageHandler(username, pre_msg.decode()) == -1:
        #                 self.request.close()
        #                 break
        #             pre_msg = self.request.recv(1024)

      except Exception as e:
         print(e)

      print('[%s] 접속종료' %self.client_address[0])
      self.userman.removeUser(username)

   def registerUsername(self):
      while True:
         self.request.send('ID:'.encode())
         username = self.request.recv(1024)
         username = username.decode().strip()
         if self.userman.addUser(username, self.request, self.client_address):
            return username

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
   print('+++ blockchain network를 시작합니다.')
   print('+++ network를 끝내려면 Ctrl-C를 누르세요.')

   try:
      server = ChatingServer((HOST, PORT), MyTcpHandler)
      server.serve_forever()
   except KeyboardInterrupt:
      print('--- blockchain network를 종료합니다.')
      server.shutdown()
      server.server_close()

runServer()

# blockchain-socket-thread

---
#### blockchain.py - blockchain의 기본 구조를 python으로 작업

#### server.py     - python socket을 이용하여 server 구현

#### client.py     - python socket,thread를 이용하여 다중 클라이언트 구현 

##### client.py 실행 접속 후
1. 'mine'  : block을 채굴하여 모든 클라이언트에 정보 전송
2. 'transaction'  : transaction을 추가할 수 있도록 input값 3개(보내는 사람,받는 사람, 보내는 양)
3. 'chain'   : 현재 blockchain의 채굴된 상황을 확인 가능

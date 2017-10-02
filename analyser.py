import time
import zmq
from operator import add
from flask import Flask

count1=0
count2=0
count3=0
cycle=1
scale=4
#scale=os.environ['scale']
port1 = "5100"
port2 = "5200"
elapsedTime=0
# Socket to talk to server
context = zmq.Context()
socket1 = context.socket(zmq.SUB)
socket1.bind("tcp://0.0.0.0:%s" % port1)
socket2 = context.socket(zmq.PUB)
socket2.connect("tcp://test:%s" % port2)
socket1.setsockopt(zmq.SUBSCRIBE, '')
messagedata = ""

app = Flask(__name__)
@app.route('/')
def api_root():
    return 'Welcome'
app.run(host='0.0.0.0')

while True:

 start_time = time.time()

 if count2<cycle:

  count2+=1

  while True:

     if count1<scale:
         count1+=1
     else:
         count1=0
         elapsedTime+=time.time() - start_time
         break

     string = socket1.recv()
     print "message received"
     print "inside %d loop" % count3

     if count3<scale:
      count3 += 1

     elif count3==scale:

      socket2.send("%d %s" % (100, "start"))
      count3 += 1


     message=string[5: len(string) - 1].split(',')
     message=map(float,message)
     if count1==1 and count2==1:
         list= message
     else:
         list=map(add, list, message)

 else:
     print [int(x / (scale*cycle)) for x in list]
     print  int(elapsedTime/cycle)
     break




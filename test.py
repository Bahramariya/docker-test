#!/usr/bin/env python

from decimal import *
import time
import psutil
#import zmq
import httplib
import json
import thread
from thread import allocate_lock

#Sets decimal to 25 digits of precision
getcontext().prec = 25
threadnum=10
num_threads = 0
thread_started = False
lock = allocate_lock()

def factorial(n):
    if n<1:
        return 1
    else:
        return n * factorial(n-1)


def bellardBig(n): #http://en.wikipedia.org/wiki/Bellard%27s_formula

    global num_threads,thread_started
    lock.acquire()
    num_threads += 1
    thread_started = True
    lock.release()
    # port1 = "5100"
    # port2 = "5200"
    # context = zmq.Context()
    # socket1 = context.socket(zmq.PUB)
    # socket1.connect("tcp://analyser:%s" % port1)
    # socket2 = context.socket(zmq.SUB)
    # socket2.bind("tcp://0.0.0.0:%s" % port2)
    # socket2.setsockopt(zmq.SUBSCRIBE, '')

    start_time = time.clock()
    pi = Decimal(0)
    k = 0
    #print "Test Started"
    #socket1.send("%d %s" % (100, psutil.cpu_percent(interval=1, percpu=True)))
    print "message sent"
    #socket2.recv()
    #print "Test Running"
    while k < n:
        # conn = httplib.HTTPConnection("analyser", 5000)
        # conn.request("GET", "/")
        # r1 = conn.getresponse()
        # conn.close()
        #print r1.status, r1.reason
        #print psutil.cpu_percent(interval=10, percpu=True)
        pi += (Decimal(-1)**k/(1024**k))*( Decimal(256)/(10*k+1) + Decimal(1)/(10*k+9) - Decimal(64)/(10*k+3) - Decimal(32)/(4*k+1) - Decimal(4)/(10*k+5) - Decimal(4)/(10*k+7) -Decimal(1)/(4*k+3))
        k += 1

    pi = pi * 1/(2**6)
    print time.clock() - start_time, "seconds"
    print psutil.cpu_times()
    print psutil.virtual_memory()
    while 1:
     try:
         conn = httplib.HTTPConnection("analyser", 5000)
         headers = {"Content-type": "application/json", "Accept": "text/plain"}
         conn.request("POST", "/results",str(time.clock() - start_time) ,headers)
         r3 = conn.getresponse().read()
         if r3=="welcome":
          conn.close()
          break
         conn.close()
     except:
         pass
    lock.acquire()
    num_threads -= 1
    lock.release()

while True:
    try:
        conn = httplib.HTTPConnection("analyser", 5000)
        conn.request("GET", "/")
        print "message sent"
        r1 = conn.getresponse().read()
        print r1
        if r1=="Yes":
            conn.request("POST", "/running","Running")
            r2 = conn.getresponse().read()
            conn.close()
            break
        conn.close()
        time.sleep(1)
    except:
        pass


for i in range (threadnum):
 thread.start_new_thread(bellardBig,(1000,))

while not thread_started:
    pass

while num_threads > 0:
   pass
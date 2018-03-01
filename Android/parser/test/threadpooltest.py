import threadpool
import time
import threading

from Queue import Queue


class Inner(object):
  def __init__(self):
    self.com_queue = Queue(2)
    self.counter = 0
    self.sizes = 5
    self.pool = threadpool.ThreadPool(3)

  def inn_do_something(self, n, com_queue):
    print "name is = %s " % n
    count = 0
    while count < 3:
      count+=1
      com_queue.put({"thread":n, "state":count})
      time.sleep(1)

    com_queue.put({"thread":n, "state":"done"})

  def proxy(self):
    while 1:
      print "queue waiting..."
      data = self.com_queue.get()
      if data["state"] == "done":
        self.counter+=1
        print "------------ ", data["thread"], " done"
        if self.counter == self.sizes:
          print "***********8 done"
          print "************ pool waiting"
          self.pool.wait()
          print "************ pool recycle done"
          break
      else:
        print "++++ ", data["thread"], " : ", data["state"]

  def thread_main(self):
    name_list = [(["pengtian", self.com_queue], None),
                 (["adaf",self.com_queue], None),
                 (["agagg",self.com_queue], None),
                 (["rutw",self.com_queue], None),
                 (["adhjk",self.com_queue], None)]

    rec = threading.Thread(target=self.proxy)
    rec.setDaemon(True)
    rec.start()

    reqs = threadpool.makeRequests(self.inn_do_something, name_list)
    [self.pool.putRequest(req) for req in reqs]

if __name__=="__main__":
  inn = Inner()
  inn.thread_main()

  time.sleep(12)

  print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
import threadpool
import time


def now_time(n):
  print 'Starting at %s' % time.ctime()
  time.sleep(n)
  print 'Ending at %s' % time.ctime()

pool = threadpool.ThreadPool(5)
reqs = threadpool.makeRequests(now_time, range(1, 11))
[pool.putRequest(req) for req in reqs]
pool.wait()
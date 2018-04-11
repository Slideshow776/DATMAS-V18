import threading, time

liste = []

def worker(num):
    """thread worker function"""
    #print('Worker: %s' % num)
    liste.append(num)
    return

start = time.time()
threads = []
for i in range(100000):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
    
#for t in threads:
    #t.join()

print(liste)
print('time took: ', time.time() - start)

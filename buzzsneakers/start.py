import time
from buzzsneakers.monitor import monitor
from buzzsneakers.backend import backend
from buzzsneakers.types import Thread
from buzzsneakers.threads import RunningThreads
import database.main as database

def Start():
    
    t = Thread(backend, None)
    t.start()
    
    """
    while True:
        time.sleep(2)


        pids = database.get_all_product_ids("products")

        for row in pids:
            if row[0] not in RunningThreads:
                RunningThreads[row[0]] = Thread(monitor, row[0])
                RunningThreads[row[0]].start()
    """
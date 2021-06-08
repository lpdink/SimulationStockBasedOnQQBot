from controller.QQBot import run_bot
from FlushThread.FlushStockInformation import flushStockInformation
from FlushThread.FlushAliveOrders import flushAliveOrders
import threading

if __name__=="__main__":
    flushAliveOrders()
    thread2 = threading.Thread(target=flushStockInformation)
    thread2.start()
    run_bot()
    print("done\n\n\n\n\ndone")

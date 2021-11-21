from controller.QQBot import run_bot
from FlushThread.FlushStockInformation import flushStockInformation
from FlushThread.FlushAliveOrders import flushAliveOrders
import threading

if __name__ == "__main__":
    print("begin run bot")
    run_bot()
    print("thanks")

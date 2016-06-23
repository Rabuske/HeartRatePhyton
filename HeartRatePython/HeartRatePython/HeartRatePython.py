from Fitbit import Fitbit
from Database import Database
import json
import threading

def callback(data):
    print(data)
    pass

db = Database()
fitbit = Fitbit(db)
thread = threading.Thread(target = fitbit.getHeartIntradayRate, args = ("2016-05-11", callback))
thread.start()
print("Hey Girl Hey")
thread.join()


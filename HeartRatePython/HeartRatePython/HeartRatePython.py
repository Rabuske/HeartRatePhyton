from Fitbit import Fitbit
from Database import Database
import json
import threading

def callback(data):
    print(data)

db = Database()
fitbit = Fitbit(db)
threading.Thread(target = fitbit.getHeartIntradayRate, args = ("2016-04-19", callback)).start()
print("Hey Girl Hey")


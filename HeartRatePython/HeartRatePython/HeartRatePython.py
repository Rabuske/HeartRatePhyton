from Fitbit import Fitbit
from Database import Database
from Plot import Plot
import datetime


db = Database()
fitbit = Fitbit(db)
plot = Plot()

while True:
    date = input("Enter a date (YYYY-MM-DD): ")

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        continue
    
    heartData = fitbit.getHeartIntradayRate(date)
    
    if heartData == None:
        print("No data returned for ", date)   
        continue

    plot.plot(heartData)
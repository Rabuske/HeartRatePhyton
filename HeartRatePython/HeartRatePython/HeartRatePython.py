from Fitbit import Fitbit
from Database import Database
import json

db = Database()
#fitbit = Fitbit(db)
#fitbit.getHeartRate("2016-04-25", "2016-04-25")

#json_data = open("data.txt").read()
#json_parsed = json.loads(json_data)
#db.saveHeartData(json_parsed)

result = db.getIntradayData("2016-04-25")
print(result)
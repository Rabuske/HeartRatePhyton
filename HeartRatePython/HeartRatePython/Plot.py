import matplotlib.pyplot as plt

class Plot(object):

    _xlabel = None
    _xtick = None

#   Fill labels to be used 
    def __init__(self):
        self._xlabel = list()
        self._xtick  = list()
        for hour in list(range(0, 24)):
            self._xlabel.append(hour*60)
            self._xtick.append(str(hour).zfill(2) + ":00")
        self._xlabel.append(1439)
        self._xtick.append("23:59")

    def plot(self, data):
        x = list()
        y = list()

        for m in list(range(0, 1441)):
            minute = m % 60
            hour   = m // 60
            fTime = str(hour).zfill(2) + ":" + str(minute).zfill(2) + ":00"
            x.append(m)
            yValue = None
            for d in data:
                if d[1] == fTime:
                    yValue = d[2]
            y.append(yValue)
        
        plt.clf()
        plt.plot(x, y)
        plt.xticks(self._xlabel, self._xtick, rotation='vertical')
        plt.show(False)



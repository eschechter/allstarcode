from datetime import datetime, date, time, timedelta

class PartOrder:
    """An order for a component"""
    def __init__(self, curState, ID, startDate, duration, rest):
        
        self.state = curState
        self.id = ID
        self.start = startDate
        self.dur = duration
        self.rest = rest

    def toString(self): 
        if (type(self.dur) is timedelta):
            return self.state + ',' + str(self.id) + ',' + self.start.strftime("%m/%d/%y %H:%M") + ',' + str(self.dur.days) + '.' + str(int(round(10*float(self.dur.seconds) / float(24*3600)))) + ',' + self.rest
        else:
            return self.state + ',' + str(self.id) + ',' + self.start.strftime("%m/%d/%y %H:%M") + ',' + str(self.dur) + ',' + self.rest


def toPartOrder1(s, l):
    curComma = s.find(',')
    curState = s[:curComma]

    nextComma = s.find(',', curComma + 1)
    ID = int(s[curComma + 1 : nextComma])

    curComma = nextComma
    nextComma = s.find(',', curComma + 1)

    startDate = datetime.strptime(s[curComma + 1: nextComma], "%m/%d/%y %H:%M")

    curComma = nextComma
    nextComma = s.find(',', curComma + 1)

    duration = s[curComma + 1 : nextComma]

    rest = s[nextComma + 1:]

    newOrder = PartOrder(curState, ID, startDate, duration, rest)
    l.append(newOrder)


def toPartOrder2(s, l):
    curComma = s.find(',')
    curState = s[:curComma]

    nextComma = s.find(',', curComma + 1)
    ID = int(s[curComma + 1 : nextComma])

    curComma = nextComma
    nextComma = s.find(',', curComma + 1)

    newDate = datetime.strptime(s[curComma + 1: nextComma], "%m/%d/%y %H:%M")

    rest = s[nextComma + 1:]

    inList = False

    for order in l:
        if order.id == ID:
            inList = True
            if order.state != curState:
                if curState == "4-Completed" or curState == "5-Withdrawn":
                    order.state = curState
                    order.dur = newDate - order.start

    if not inList:
        if curState == "2-In Process" or curState == "3-SAP Entry":
            newOrder = PartOrder(curState, ID, newDate, None, rest)
            l.append(newOrder)
        elif curState == "4-Completed" or curState == "5-Withdrawn":
            newOrder = PartOrder(curState, ID, newDate, 0, rest)
            l.append(newOrder)

partOrderList = []

path1 = raw_input("Pick an old result to update. If starting from scratch, leave blank. \n")

if path1 != '':
    g = open(path1, 'r')
    for line in g:
        toPartOrder1(line, partOrderList)


path2 = raw_input("Pick a snapshot to update results with. \n")

#fun change

f = open(path2, 'r')

for line in f:
    if line[0] != "S":
        toPartOrder2(line, partOrderList)

r = open(str(datetime.now().strftime("%m-%d-%y_%H-%M-%S")) + '.csv', 'a')

for part in partOrderList:
    r.write(part.toString())


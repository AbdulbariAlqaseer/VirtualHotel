import datetime,time

class Code:
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Code.__instance == None:
            Code()
        return Code.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if Code.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Code.__instance = self
    
    lis = [
        'v', 'a', 'H', 'c', 'N', 'l', 'X', 'g', 'D', '6',
        'o', '9', 'w', 'u', 's', 'F', 'S', 'j', 'G', 'd',
        'k', '5', 'R', '0', 'C', '7', 'I', 'b', 'q', 'K',
        'V', 'f', 'Z', 'M', 'L', 'i', 'T', 'B', '2', 'h',
        'J', 'Y', 'n', 'e', 'y', '8', 'E', '4', 'O', 'W',
        'p', '3', 'm', 'x', 't', 'U', 'A', 'P', '1', 'r',
        'Q', 'z'
        ]
    count = 0
    lastTime = None

    def datetimeCode(self):
        t = datetime.datetime.now()
        if self.lastTime != None and t.second == self.lastTime.second :
            if(self.count > 61):
                time.sleep(1)
                t = datetime.datetime.now()
                self.lastTime = t
                self.count = 0
            x = self.count
            self.count += 1
        else :
            self.count = 0
            x = self.count
            self.count += 1
            self.lastTime = t
        return (
            self.lis[-1*t.month]+self.lis[t.day+10]+
            self.lis[-1*t.hour-10]+self.lis[-t.minute]+
            self.lis[x]+self.lis[t.second]
            )
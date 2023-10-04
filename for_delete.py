from datetime import *
#from time import time
import pytz
def test(a):
    a = int(a)
    return False,a
'''
a,b,c = "4","vsbs",3.00000000001
d = {
    "d1" : "23rf",
    #"d2" : None,
    1 : [1,2,3,4,5],
    'a' : [2,6,8]
}
print("a = " + str(a),"b = " + str(b),"c = " + str(c))
print(d)
print(d.get("d2"),isinstance(d.get("d2"),object))
if not d.get("d2") :
    print("inside if")
e = "2020-12-02"
print(e[0:4])
print(e[5:7])
print(e[8::])
print(date.today().year)
print(type(test(a)))
t = test(a)
print(t[0],t[1])
'''
'''import time

#print(time.timezone)
current_utc = time.gmtime()
nine_utc = time.struct_time(
    (current_utc.tm_year,current_utc.tm_mon,current_utc.tm_mday,
    21,0,0,
    current_utc.tm_wday,current_utc.tm_yday,current_utc.tm_isdst)
    )
print(current_utc)
print(nine_utc)
print(current_utc > nine_utc)
'''
'''for i in pytz.all_timezones:
    if i.startswith("Asia/Damascus"):
        print(i)
print(datetime.now(pytz.timezone("Asia/Damascus")))
utcNow = datetime.now(pytz.timezone("UTC"))

print(utcNow)
print(utcNow.date())
print(utcNow.time())
t1 = time(21,0,0,0)
t2 = time(utcNow.time().hour,utcNow.time().minute,utcNow.time().second,utcNow.time().microsecond)

print("time 9 oclock : ",t1)
print(utcNow.time() == t2)
'''
def test_maince_date():
    t = date(2021,1,1)
    t2 = date(2021,4,1)
    days = timedelta(days = 1)
    print(t,t2)
    print((t - t2).days)
    t = t - days
    print(type(t),t)
def check_register_age(birth_date):
    bdate =date(int(birth_date[0:4]),int(birth_date[5:7]),int(birth_date[8::]))
    today = datetime.now(pytz.timezone("UTC")).date()
    print(today - bdate , "\n18 years is days : " , 18*365.25)
    if bdate.year > (today.year - 18):
        print(1)
        return False
    if bdate.year == (today.year - 18):
        if bdate.month > today.month:
            print(2)
            return False
        if bdate.month == today.month:
            if bdate.day > today.day:
                print(3)
                return False
    return True
def test_calc_age():
    t = date(2010,9,20)
    if check_register_age(t):
        print("bigger 18")
    else:
        print("smaller 18")
def test_if_none():
    x = 1
    y = "dqad"
    z = None
    if not (x and y and z):
        print("exist none")
    else:
        print("not exist none")
def isoformat():
    d = date().fromisoformat("2000-10-12")
    print(d)
#test_if_none()
#test_calc_age()
#test_maince_date()
#isoformat()
#print(check_register_age("2003-09-03"))

dt = datetime(2021,10,1,12,0,0,0,pytz.timezone("UTC"))
dt = dt.replace(hour=14)
print(dt)
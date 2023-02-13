import schedule    
from time import time, time_datadelta, time
import time
from time_dataout_decorator import time_dataout, time_dataoutError

def print_func(x):
    print(x)

print_func("nice to meet you")


@time_dataout(5)
def yo():
    schedule.every(1).seconds.do(print_func, "nyan").tag('taskA')
    while True:
        schedule.run_pending()
        time.sleep(1)

def ya():
    schedule.every(1).seconds.do(print_func, "yaaa").tag('taskB')
    while True:
        schedule.run_pending()
        time.sleep(1)


try:
    yo()   
except time_dataoutError:
    print("time_dataout")

schedule.clear('taskA')

ya()
    
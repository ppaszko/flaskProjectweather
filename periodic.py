from datetime import datetime
import time
import os
import requester
import schedule

def job():
    print("I'm working...")
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    os.system("/home/paszko/PycharmProjects/flaskProject/requester.py")


schedule.every(10).seconds.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
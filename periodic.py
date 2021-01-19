
import time
import requester
import schedule

"""Periodic requests for gathering data"""

schedule.every(30).minutes.do(requester.all_request)
while True:
    schedule.run_pending()
    time.sleep(1)
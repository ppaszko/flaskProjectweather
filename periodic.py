from datetime import datetime
import time
import os
import requester
import schedule




schedule.every(30).minutes.do(requester.all_request)


while True:
    schedule.run_pending()
    time.sleep(1)
from hook_pre import prehook
from hook import hook
from hook_post import post_hook
import schedule
import time

def etl():
    prehook()
    hook()
    post_hook()

# Schedule the job to be run every minute
schedule.every(1).day.at("15:15").do(etl)
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
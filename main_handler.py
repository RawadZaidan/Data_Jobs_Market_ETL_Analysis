from hook_pre import prehook
from hook import hook
from hook_post import post_hook
import time

if __name__ == "__main__":
    while True:
        now = time.localtime()
        if now.tm_hour == 6 and now.tm_min == 0:
            prehook()
            hook()
            post_hook()
            time.sleep(22 * 60 * 60)
        else:
            # Sleep for a minute and check again
            time.sleep(60)
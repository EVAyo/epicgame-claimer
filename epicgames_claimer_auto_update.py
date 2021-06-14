import os
import signal
import time
import urllib.request

import schedule

if __name__ == "__main__":
    def quit(self, signum = None, frame = None) -> None:
        try:
            self.close_browser()
        except:
            pass
        exit(1)
    def update() -> None:
        epicgames_claimer_py_link = "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/master/epicgames_claimer.py"
        try:
            urllib.request.urlretrieve(epicgames_claimer_py_link, filename="epicgames_claimer.py")
        except:
            pass
    def run() -> None:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        try:
            signal.signal(signal.SIGBREAK, quit)
        except AttributeError:
            pass
        try:
            signal.signal(signal.SIGHUP, quit)
        except AttributeError:
            pass
        def everyday_job() -> None:
            update()
            os.system("python epicgames_claimer.py --once")
        everyday_job()
        schedule.every().day.at("09:00").do(everyday_job)
        while True:
            schedule.run_pending()
            time.sleep(1)
    update()
    run()

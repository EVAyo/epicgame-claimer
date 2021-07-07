import argparse
import importlib
import os
import signal
import time

import schedule
import update_check


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Claim weekly free games from Epic Games Store.",
        usage="python epicgames_claimer_auto_update.py [-h] [-hf] [-c CHROMIUM_PATH] [-r RUN_AT] [-o]"
    )
    parser.add_argument("-hf", "--headful", action="store_true", help="run Chromium in headful mode")
    parser.add_argument("-c", "--chromium-path", type=str, help="set path to Chromium executable")
    parser.add_argument("-r", "--run-at", type=str, default="09:00", help="set daily check and claim time(HH:MM, default: 09:00)")
    parser.add_argument("-o", "--once", action="store_true", help="claim once then exit")    
    args = parser.parse_args()
    def epicgames_claimer_exists() -> bool:
        if os.path.exists("epicgames_claimer.py") and os.path.getsize("epicgames_claimer.py") > 0:
            return True
        else:
            return False
    if not epicgames_claimer_exists():
        open("epicgames_claimer.py", "w").close()
        try:
            update_check.checkForUpdates("epicgames_claimer.py", "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/dev/epicgames_claimer.py")
        except:
            print("Can not download \"epicgames_claimer.py\". Please try it manually.")
            exit(1)
    import epicgames_claimer
    def update_epicgmaes_claimer() -> None:
        try:
            if update_check.checkForUpdates("epicgames_claimer.py", "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/dev/epicgames_claimer.py"):
                importlib.reload(epicgames_claimer)
                epicgames_claimer.epicgames_claimer.log("\"epicgames_claimer.py\" has been updated.")
        except Exception as e:
            epicgames_claimer.epicgames_claimer.log("Update \"epicgames_claimer.py\" failed. {}: {}".format(e.__class__.__name__, e), level="warning")
    def run_once() -> None:
        claimer = epicgames_claimer.epicgames_claimer(headless=(not args.headful), chromium_path=args.chromium_path)
        signal.signal(signal.SIGINT, claimer._quit)
        signal.signal(signal.SIGTERM, claimer._quit)
        try:
            signal.signal(signal.SIGBREAK, claimer._quit)
        except AttributeError:
            pass
        try:
            signal.signal(signal.SIGHUP, claimer._quit)
        except AttributeError:
            pass
        claimer.logged_claim()
        claimer.close_browser()
    def update_and_run_once() -> None:
        update_epicgmaes_claimer()
        run_once()
    epicgames_claimer.epicgames_claimer.log("Claimer is starting...")
    claimer_for_login = epicgames_claimer.epicgames_claimer(headless=(not args.headful), chromium_path=args.chromium_path)
    if claimer_for_login.logged_login():
        claimer_for_login.close_browser()
        epicgames_claimer.epicgames_claimer.log("Claimer has started. Run at {} everyday.".format(args.run_at))
        update_and_run_once()
        if not args.once:
            schedule.every().day.at(args.run_at).do(update_and_run_once)
            while True:
                schedule.run_pending()
                time.sleep(1)        
    else:
        exit(1)

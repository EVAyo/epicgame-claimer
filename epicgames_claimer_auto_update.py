import argparse
import importlib
import signal
import time

import schedule
import update_check

import epicgames_claimer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Claim weekly free games from Epic Games Store.",
        usage="python epicgames_claimer_auto_update.py [-h] [-hf] [-c CHROMIUM_PATH] [-r RUN_AT] [-o]"
    )
    parser.add_argument("-hf", "--headful", action="store_true", help="run Chromium in headful mode")
    parser.add_argument("-c", "--chromium-path", type=str, help="set path to Chromium executable")
    parser.add_argument("-r", "--run-at", type=str, default="09:00", help="set daily check and claim time(HH:MM)")
    parser.add_argument("-o", "--once", action="store_true", help="claim once then exit")    
    args = parser.parse_args()
    def update_epicgmaes_claimer() -> None:
        try:
            update_check.checkForUpdates("epicgames_claimer.py", "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/dev/epicgames_claimer.py")
            importlib.reload(epicgames_claimer)
        except Exception as e:
            epicgames_claimer.epicgames_claimer.log("Update failed. {}: {}".format(e.__class__.__name__, e), level="warning")
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
    def run_once_with_update() -> None:
        update_epicgmaes_claimer()
        run_once()
    epicgames_claimer.epicgames_claimer.log("Claimer is starting...")
    claimer_for_login = epicgames_claimer.epicgames_claimer(headless=(not args.headful), chromium_path=args.chromium_path)
    if claimer_for_login.logged_login():
        claimer_for_login.close_browser()
        epicgames_claimer.epicgames_claimer.log("Claimer has started.")
        if args.once:
            run_once_with_update()
        else:
            run_once_with_update()
            schedule.every().day.at(args.run_at).do(run_once_with_update)
            while True:
                schedule.run_pending()
                time.sleep(1)        
    else:
        exit(1)

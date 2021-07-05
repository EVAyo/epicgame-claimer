import argparse
import importlib
import time

import schedule
import update_check

import epicgames_claimer


def run_auto_update(claimer: epicgames_claimer.epicgames_claimer):
    claimer.run(args.run_at, once=True)
    try:
        update_check.checkForUpdates("epicgames_claimer.py", "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/dev/epicgames_claimer.py")
        importlib.reload(epicgames_claimer)
        claimer = epicgames_claimer.epicgames_claimer(headless=(not args.headful), chromium_path=args.chromium_path)
    except Exception as e:
        epicgames_claimer.epicgames_claimer.log("Update failed. {}: {}".format(e.__class__.__name__, e), level="warning")


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
    epicgames_claimer.epicgames_claimer.log("Claimer is starting...")
    claimer = epicgames_claimer.epicgames_claimer(headless=(not args.headful), chromium_path=args.chromium_path)
    if claimer.logged_login():
        epicgames_claimer.epicgames_claimer.log("Claimer has started.")
        if args.once:
            run_auto_update(claimer)
        else:
            def job():
                run_auto_update(claimer)
            job()
            schedule.every().day.at(args.run_at).do(job)
            while True:
                schedule.run_pending()
                time.sleep(1)        
    else:
        exit(1)

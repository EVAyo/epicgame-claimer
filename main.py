import importlib
import time
from pyppeteer.errors import BrowserError

import schedule
import update_check

import epicgames_claimer


args = epicgames_claimer.get_args(include_auto_update=True)
if args.username != None and args.password == None:
    raise ValueError("Must input both username and password.")
if args.username == None and args.password != None:
    raise ValueError("Must input both username and password.")
interactive = True if args.username == None else False
data_dir = "User_Data/Default" if interactive else None

def update() -> None:
    try:
        if update_check.checkForUpdates("epicgames_claimer.py", "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/master/epicgames_claimer.py"):
            importlib.reload(epicgames_claimer)
            epicgames_claimer.epicgames_claimer.log("\"epicgames_claimer.py\" has been updated.")
    except Exception as e:
        epicgames_claimer.epicgames_claimer.log("Update \"epicgames_claimer.py\" failed. {}: {}".format(e.__class__.__name__, e), level="warning")

def run(claimer: epicgames_claimer.epicgames_claimer) -> None:
    if args.auto_update:
        claimer.close_browser()
        update()
        for i in range(3):
            try:
                claimer = epicgames_claimer.epicgames_claimer(data_dir, headless=not args.no_headless, chromium_path=args.chromium_path)
                break
            except BrowserError as e:
                epicgames_claimer.epicgames_claimer.log(str(e).replace("\n", " "), "warning")
                if i == 2:
                    epicgames_claimer.epicgames_claimer.log("Failed to open the browser.", "error")
                    return
    claimer.run_once(interactive, args.username, args.password)

def scheduled_run(claimer: epicgames_claimer.epicgames_claimer, at: str):
    claimer.add_quit_signal()
    schedule.every().day.at(at).do(run, claimer)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main() -> None:
    epicgames_claimer.epicgames_claimer.log("Claimer is starting...")
    if args.auto_update:
        update()
    claimer = epicgames_claimer.epicgames_claimer(data_dir, headless=not args.no_headless, chromium_path=args.chromium_path)
    if args.once == True:
        epicgames_claimer.epicgames_claimer.log("Claimer has started.")
        claimer.run_once(interactive, args.username, args.password)
        epicgames_claimer.epicgames_claimer.log("Claim completed.")
    else:
        epicgames_claimer.epicgames_claimer.log("Claimer has started. Run at {} everyday.".format(args.run_at))
        claimer.run_once(interactive, args.username, args.password)
        scheduled_run(claimer, args.run_at)


if __name__ == "__main__":
    main()

import argparse
import importlib
import time

import schedule
import update_check

import epicgames_claimer


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Claim weekly free games from Epic Games Store.")
    parser.add_argument("-n", "--no-headless", action="store_true", help="run the browser with GUI")
    parser.add_argument("-c", "--chromium-path", type=str, help="set path to browser executable")
    parser.add_argument("-r", "--run-at", type=str, default="09:00", help="set daily check and claim time(HH:MM, default: 09:00)")
    parser.add_argument("-o", "--once", action="store_true", help="claim once then exit")
    parser.add_argument("-na", "--no-auto-update", action="store_true", help="disable auto update")
    parser.add_argument("-u", "--username", type=str, help="set username/email")
    parser.add_argument("-p", "--password", type=str, help="set password")
    args = parser.parse_args()
    return args


def main() -> None:
    args = get_args()
    interactive = True if args.username == None else False
    data_dir = "User_Data/Default" if interactive else None
    def update() -> None:
        if not args.no_auto_update:
            try:
                if update_check.checkForUpdates("epicgames_claimer.py", "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/master/epicgames_claimer.py"):
                    importlib.reload(epicgames_claimer)
                    epicgames_claimer.epicgames_claimer.log("\"epicgames_claimer.py\" has been updated.")
            except Exception as e:
                epicgames_claimer.epicgames_claimer.log("Update \"epicgames_claimer.py\" failed. {}: {}".format(e.__class__.__name__, e), level="warning")
    def run(claimer: epicgames_claimer.epicgames_claimer) -> None:
        claimer.close_browser()
        update()
        claimer = epicgames_claimer.epicgames_claimer(data_dir, headless=not args.no_headless, chromium_path=args.chromium_path)
        claimer.run_once(interactive, args.username, args.password)
    def scheduled_run(claimer: epicgames_claimer.epicgames_claimer, at: str):
        claimer.add_quit_signal()
        schedule.every().day.at(at).do(run, claimer)
        while True:
            schedule.run_pending()
            time.sleep(1)
    epicgames_claimer.epicgames_claimer.log("Claimer is starting...")
    update()
    claimer = epicgames_claimer.epicgames_claimer(data_dir, headless=not args.no_headless, chromium_path=args.chromium_path)
    if args.once == True:
        epicgames_claimer.epicgames_claimer.log("Claimer has started.")
        claimer.run_once(interactive, args.username, args.password)
        epicgames_claimer.epicgames_claimer.log("Claim has been completed.")
    else:
        epicgames_claimer.epicgames_claimer.log("Claimer has started. Run at {} everyday.".format(args.run_at))
        claimer.run_once(interactive, args.username, args.password)
        scheduled_run(claimer, args.run_at)


if __name__ == "__main__":
    main()

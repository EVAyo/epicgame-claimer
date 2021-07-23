import argparse
import importlib
import signal
import time

import schedule
import update_check

import epicgames_claimer


def update() -> None:
    try:
        if update_check.checkForUpdates("epicgames_claimer.py", "https://raw.githubusercontent.com/luminoleon/epicgames-claimer/master/epicgames_claimer.py"):
            importlib.reload(epicgames_claimer)
            epicgames_claimer.epicgames_claimer.log("\"epicgames_claimer.py\" has been updated.")
    except Exception as e:
        epicgames_claimer.epicgames_claimer.log("Update \"epicgames_claimer.py\" failed. {}: {}".format(e.__class__.__name__, e), level="warning")


def login() -> bool:
    claimer_for_login = epicgames_claimer.epicgames_claimer(data_dir="User_Data/Default", headless=not args.no_headless, chromium_path=args.chromium_path)
    if claimer_for_login.logged_login():
        claimer_for_login.close_browser()
        return True
    else:
        claimer_for_login.close_browser()
        return False


def run_once(auto_update_enabled: bool, headless: bool, chromium_path: str) -> None:
    if auto_update_enabled:
        update()
    claimer = epicgames_claimer.epicgames_claimer(data_dir="User_Data/Default", headless=headless, chromium_path=chromium_path)
    signal.signal(signal.SIGINT, claimer._quit)
    signal.signal(signal.SIGTERM, claimer._quit)
    if "SIGBREAK" in dir(signal):
        signal.signal(signal.SIGBREAK, claimer._quit)
    if "SIGHUP" in dir(signal):
        signal.signal(signal.SIGHUP, claimer._quit)
    claimer.logged_claim()
    claimer.close_browser()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Claim weekly free games from Epic Games Store.")
    parser.add_argument("-n", "--no-headless", action="store_true", help="run the browser with GUI")
    parser.add_argument("-c", "--chromium-path", type=str, help="set path to browser executable")
    parser.add_argument("-r", "--run-at", type=str, default="09:00", help="set daily check and claim time(HH:MM, default: 09:00)")
    parser.add_argument("-o", "--once", action="store_true", help="claim once then exit")
    parser.add_argument("-na", "--no-auto-update", action="store_true", help="disable auto update")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    epicgames_claimer.epicgames_claimer.log("Claimer is starting...")
    if not args.no_auto_update:
        update()
    if login():
        epicgames_claimer.epicgames_claimer.log("Claimer has started. Run at {} everyday.".format(args.run_at))
        run_once(False, not args.no_headless, args.chromium_path)
        if not args.once:
            schedule.every().day.at(args.run_at).do(run_once, not args.no_auto_update, not args.no_headless, args.chromium_path)
            while True:
                schedule.run_pending()
                time.sleep(1)
    else:
        exit(1)

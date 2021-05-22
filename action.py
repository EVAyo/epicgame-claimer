import os

import epicgames_claimer


def log(text: str, level: str = "message") -> None:
    if level == "message":
        print("{}".format(text))
    elif level == "warning":
        print("\033[33mWarning: {}\033[0m".format(text))
    elif level == "error":
        print("\033[31mError: {}\033[0m".format(text))


if __name__ == "__main__":
    EMAIL = os.environ["EMAIL"]
    PASSWORD = os.environ["PASSWORD"]

    claimer = epicgames_claimer.epicgames_claimer(sandbox=True)
    
    def login():
        for _ in range(3):
            try:
                claimer.login(EMAIL, PASSWORD, two_fa_enabled=False, remember_me=False)
                log("Login successed.")
                return
            except Exception as e:
                log("Login failed({}).".format(e), "warning")
        epicgames_claimer.log("Login failed.", "error")
        exit(1)
    
    def claim():
        for _ in range(5):
            try:
                claimed_game_titles = claimer.claim()
                if len(claimed_game_titles) > 0:
                    log("{} has been claimed.".format(str(claimed_game_titles).strip("[]").replace("'", "")))
                else:
                    log("There is no game need to be claimed.")
                return
            except Exception as e:
                log("{}.".format(str(e).rstrip(".")), level="warning")
        log("Claim failed.", "error")
        exit(1)

    login()
    claim()

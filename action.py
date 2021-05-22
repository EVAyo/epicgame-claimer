import os

import epicgames_claimer


if __name__ == "__main__":
    EMAIL = os.environ["EMAIL"]
    PASSWORD = os.environ["PASSWORD"]

    claimer = epicgames_claimer.epicgames_claimer()
    
    def login():
        for _ in range(5):
            try:
                claimer.login(EMAIL, PASSWORD, two_fa_enabled=False)
                epicgames_claimer.log("Login successed.")
                return
            except Exception as e:
                epicgames_claimer.log("Login failed({}).".format(e), "warning")
        epicgames_claimer.log("Login failed.", "error")
        exit(1)
    
    def claim():
        for _ in range(5):
            try:
                claimed_game_titles = claimer.claim()
                if len(claimed_game_titles) > 0:
                    epicgames_claimer.log("{} has been claimed.".format(str(claimed_game_titles).strip("[]").replace("'", "")))
                else:
                    epicgames_claimer.log("There is no game need to be claimed.")
                return
            except Exception as e:
                epicgames_claimer.log("{}.".format(str(e).rstrip(".")), level="warning")
        epicgames_claimer.log("Claim failed.", "error")
        exit(1)

    login()
    claim()

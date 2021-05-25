import getpass

import epicgames_claimer


def log(text: str, level: str = "message") -> None:
    if level == "message":
        print("{}".format(text))
    elif level == "warning":
        print("\033[33mWarning: {}\033[0m".format(text))
    elif level == "error":
        print("\033[31mError: {}\033[0m".format(text))


if __name__ == "__main__":
    claimer = epicgames_claimer.epicgames_claimer(headless=True)
    
    def login():
        for _ in range(3):
            try:
                if not claimer.is_loggedin():
                    EMAIL = input("Email: ")
                    PASSWORD = getpass("Password: ")
                    claimer.login(EMAIL, PASSWORD)
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
                    log("There is no game to be claimed.")
                return
            except Exception as e:
                log("{}.".format(str(e).rstrip(".")), level="warning")
        log("Claim failed.", "error")
        exit(1)

    login()
    claim()

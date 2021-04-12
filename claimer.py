import asyncio
from typing import Union
from pyppeteer import launch, launcher
import time
from getpass import getpass
import schedule
import json
import os


class epic_claimer:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.browser = self.loop.run_until_complete(
            launch(options={
                "args": ["--no-sandbox"],
                "headless": False
            },
                   userDataDir="userdata"))
        self.page = self.loop.run_until_complete(self.browser.pages())[0]
        if not os.path.exists("config.json"):
            with open("config.json", "w") as config_json:
                self.config = {"email": None, "password": None}
                config_json.write(
                    json.dumps(self.config, indent=4, separators=(',', ': ')))
        else:
            with open("config.json", "r") as config_json:
                self.config = json.loads(config_json.read())

    def close(self) -> None:
        self.loop.run_until_complete(self.browser.close())

    def log(self, text: str, level: str = "message") -> None:
        localtime = time.asctime(time.localtime(time.time()))
        if level == "message":
            print("[{}] {}".format(localtime, text))
        elif level == "warning":
            print("[{}] \033[33mWarning: {}\033[0m".format(localtime, text))
        elif level == "error":
            print("[{}] \033[31mError: {}\033[0m".format(localtime, text))

    def retry(self,
              func_try: function,
              times: int,
              func_except: Union[function, None] = None,
              func_finally: Union[function, None] = None) -> None:
        for i in range(times):
            try:
                func_try()
                break
            except:
                func_except()
            finally:
                func_finally()

    async def type_async(self,
                         selector: str,
                         text: str,
                         sleep_time: Union[int, float] = 0) -> None:
        await self.page.waitForSelector(selector)
        time.sleep(sleep_time)
        await self.page.type(selector, text)

    async def click_async(self,
                          selector: str,
                          sleep_time: Union[int, float] = 2) -> None:
        await self.page.waitForSelector(selector)
        time.sleep(sleep_time)
        await self.page.click(selector)

    async def get_text_async(self,
                             selector: str,
                             property: str = "textContent") -> str:
        await self.page.waitForSelector(selector)
        return await (await (await self.page.querySelector(selector)
                             ).getProperty(property)).jsonValue()

    async def detect_async(self,
                           selector: str,
                           timeout: Union[int, None] = None) -> str:
        try:
            if timeout != None:
                await self.page.waitForSelector(selector,
                                                options={"timeout": timeout})
            else:
                await self.page.waitForSelector(selector)
            return True
        except:
            return False

    async def try_click_async(self,
                              selector: str,
                              sleep_time: Union[int, float] = 2) -> bool:
        if await self.detect_async(selector):
            time.sleep(sleep_time)
            await self.click_async(selector)
            return True
        return False

    async def login_async(self) -> bool:
        for i in range(0, 5):
            try:
                await self.page.goto("https://www.epicgames.com/",
                                     options={"timeout": 120000})
                if (await self.get_text_async(
                        "#user > ul > li > a",
                        "href")) != "https://www.epicgames.com/login":
                    return True
                await self.click_async("#user")
                await self.click_async("#login-with-epic")
                config_changed = False
                if self.config["email"] == None or self.config[
                        "password"] == None:
                    self.config["email"] = input("Email: ")
                    self.config["password"] = getpass("Password: ")
                    config_changed = True
                await self.type_async("#email", self.config["email"])
                await self.type_async("#password", self.config["password"])
                await self.click_async("#sign-in[tabindex=\"0\"]")
                if await self.detect_async("#code"):
                    await self.type_async("#code", input("2FA code: "))
                    await self.click_async("#continue[tabindex=\"0\"]")
                await self.page.waitForSelector("#user")
                if config_changed == True:
                    with open("config.json", "w") as config_json:
                        config_json.write(
                            json.dumps(self.config,
                                       indent=4,
                                       separators=(',', ': ')))
                self.log(
                    "Login successed. "
                    "Now you can press Ctrl + P + Q to switch to the background."
                )
                return True
            except Exception as e:
                if i < 4:
                    self.log(
                        "Something wrong in login({}: {}). Login failed. Retrying..."
                        .format(e.__class__.__name__, e),
                        level="warning")
                    with open("config.json", "r") as config_json:
                        self.config = json.loads(config_json.read())
                else:
                    self.log(
                        "Something wrong in login({}: {}). Login failed. Will retry next time."
                        .format(e.__class__.__name__, e),
                        level="error")
                    return False

    def login(self) -> bool:
        return self.loop.run_until_complete(self.login_async())

    async def order_async(self, title: str) -> None:
        if await self.detect_async(
                "#purchase-app div.navigation-element.complete"):
            if "0.00" in (await self.get_text_async(
                    "#purchase-app div.price-row-container.total")):
                await self.click_async(
                    "#purchase-app > div > div.order-summary-container "
                    "> div.order-summary-card > div.order-summary-card-inner "
                    "> div.order-summary-content > div > div > button:not([disabled])"
                )
                await self.page.waitForSelector(
                    "div[class*=DownloadLogoAndTitle__header]")
                self.log("\"{}\" has been claimed.".format(title))

    async def claim_async(self) -> None:
        for i in range(0, 5):
            try:
                await self.page.goto(
                    "https://www.epicgames.com/store/zh-CN/free-games",
                    options={"timeout": 120000})
                await self.page.waitForSelector(
                    "div[data-component=CustomDiscoverModules] > "
                    "div:nth-child(2) "
                    "div[data-component=CardGridDesktopBase]")
                item_list = await self.page.querySelectorAll(
                    "div[data-component=CustomDiscoverModules] > "
                    "div:nth-child(2) "
                    "div[data-component=CardGridDesktopBase]")
                for index in range(0, len(item_list)):
                    await self.page.waitForSelector(
                        "div[data-component=CustomDiscoverModules] > "
                        "div:nth-child(2) "
                        "div[data-component=CardGridDesktopBase]")
                    item = (await self.page.querySelectorAll(
                        "div[data-component=CustomDiscoverModules] > "
                        "div:nth-child(2) "
                        "div[data-component=CardGridDesktopBase]"))[index]
                    await item.click()
                    await self.try_click_async(
                        "div[class*=WarningLayout__layout] Button")
                    game_title = (await self.page.title()).strip("《》")
                    if await self.try_click_async(
                            "button[data-testid=purchase-cta-button]:"
                            "not([disabled]):nth-child(1)"):
                        await self.order_async(game_title)
                    elif await self.try_click_async(
                            "button[data-testid=purchase-cta-button]:"
                            "not([disabled]):nth-child(2)"):
                        await self.order_async(game_title)
                    await self.page.goto(
                        "https://www.epicgames.com/store/zh-CN/free-games",
                        options={"timeout": 120000})
                return
            except Exception as e:
                if i < 4:
                    self.log(
                        "Something wrong in claim({}: {}). Claim failed. Retrying..."
                        .format(e.__class__.__name__, e),
                        level="warning")
                else:
                    self.log(
                        "Something wrong in claim({}: {}). Claim failed. Will retry next time."
                        .format(e.__class__.__name__, e),
                        level="error")

    def claim(self) -> None:
        self.loop.run_until_complete(self.claim_async())


if __name__ == "__main__":
    launcher.DEFAULT_ARGS.remove("--enable-automation")

    def claimer_job():
        claimer = epic_claimer()
        if claimer.login():
            claimer.claim()
        claimer.close()

    claimer_job()

    schedule.every().day.at("09:00").do(claimer_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

import asyncio
from pyppeteer import launch, launcher
import time
from getpass import getpass
import schedule
import json
import os


class epic_claimer:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.browser = self.loop.run_until_complete(
            launch(options={"args": ["--no-sandbox"],
                            "headless": False}, userDataDir="userdata")
        )
        self.page = self.loop.run_until_complete(self.browser.pages())[0]
        if not os.path.exists("config.json"):
            with open("config.json", "w") as config_json:
                self.config = {"email": None, "password": None}
                config_json.write(json.dumps(
                    self.config, indent=4, separators=(',', ': ')))
        else:
            with open("config.json", "r") as config_json:
                self.config = json.loads(config_json.read())

    def close(self):
        self.loop.run_until_complete(self.browser.close())

    def log(self, text):
        localtime = time.asctime(time.localtime(time.time()))
        print("[{}] {}".format(localtime, text))

    def retry(func_try, times, func_except=None, func_finally=None):
        for i in range(times):
            try:
                func_try()
                break
            except:
                func_except()
            finally:
                func_finally()

    async def type_async(self, selector, text, sleep_time=0):
        await self.page.waitForSelector(selector)
        time.sleep(sleep_time)
        await self.page.type(selector, text)

    async def click_async(self, selector, sleep_time=2):
        await self.page.waitForSelector(selector)
        time.sleep(sleep_time)
        await self.page.click(selector)

    async def get_text_async(self, selector, property="textContent"):
        await self.page.waitForSelector(selector)
        return await (await (await self.page.querySelector(selector)).getProperty(property)).jsonValue()

    async def detect_async(self, selector, timeout=None):
        try:
            if timeout != None:
                await self.page.waitForSelector(selector, options={"timeout": timeout})
            else:
                await self.page.waitForSelector(selector)
            return True
        except:
            return False

    async def try_click_async(self, selector, sleep_time=2):
        if await self.detect_async(selector):
            time.sleep(sleep_time)
            await self.click_async(selector)
            return True
        return False

    async def login_async(self):
        for i in range(0, 5):
            try:
                await self.page.goto("https://www.epicgames.com/", options={"timeout": 120000})
                if (await self.get_text_async("#user > ul > li > a", "href")) != "https://www.epicgames.com/login":
                    return True
                await self.click_async("#user")
                await self.click_async("#login-with-epic")
                config_changed = False
                if self.config["email"] == None or self.config["password"] == None:
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
                        config_json.write(json.dumps(
                            self.config, indent=4, separators=(',', ': ')))
                self.log(
                    "Login successed. Now you can press Ctrl + P + Q to switch to the background.")
                return True
            except Exception as e:
                if i < 4:
                    self.log("{}: {} Login failed. Retrting...".format(
                        e.__class__.__name__, e))
                    with open("config.json", "r") as config_json:
                        self.config = json.loads(config_json.read())
                else:
                    self.log("{}: {} Login failed.".format(
                        e.__class__.__name__, e))
                    return False

    def login(self):
        return self.loop.run_until_complete(self.login_async())

    async def order_async(self, title):
        if await self.detect_async("#purchase-app div.navigation-element.complete"):
            if "0.00" in (await self.get_text_async("#purchase-app div.price-row-container.total")):
                await self.click_async("#purchase-app > div > div.order-summary-container "
                                       "> div.order-summary-card > div.order-summary-card-inner "
                                       "> div.order-summary-content > div > div > button:not([disabled])")
                await self.page.waitForSelector("div[class*=DownloadLogoAndTitle__header]")
                self.log("{} Claim successed.".format(title))

    async def claim_async(self):
        for i in range(0, 5):
            try:
                await self.page.goto("https://www.epicgames.com/store/zh-CN/free-games",
                                     options={"timeout": 120000}
                                     )
                await self.page.waitForSelector("div[data-component=CustomDiscoverModules] > div:nth-child(2) "
                                                "div[data-component=CardGridDesktopBase]"
                                                )
                item_list = await self.page.querySelectorAll("div[data-component=CustomDiscoverModules] > "
                                                             "div:nth-child(2) div[data-component=CardGridDesktopBase]"
                                                             )
                for index in range(0, len(item_list)):
                    await self.page.waitForSelector("div[data-component=CustomDiscoverModules] > div:nth-child(2) "
                                                    "div[data-component=CardGridDesktopBase]"
                                                    )
                    item = (await self.page.querySelectorAll("div[data-component=CustomDiscoverModules] > "
                                                             "div:nth-child(2) div[data-component=CardGridDesktopBase]")
                            )[index]
                    await item.click()
                    await self.try_click_async("div[class*=WarningLayout__layout] Button")
                    game_title = await self.get_text_async("#storeNavListBox span[data-component=\"Message\"]")
                    if await self.try_click_async("button[data-testid=purchase-cta-button]:not([disabled]):nth-child(1)"):
                        await self.order_async(game_title)
                    elif await self.try_click_async("button[data-testid=purchase-cta-button]:not([disabled]):nth-child(2)"):
                        await self.order_async(game_title)
                    await self.page.goto("https://www.epicgames.com/store/zh-CN/free-games",
                                         options={"timeout": 120000}
                                         )
                return
            except Exception as e:
                if i < 4:
                    self.log("{}: {} Claim failed. Retrying...".format(
                        e.__class__.__name__, e))
                else:
                    self.log("{}: {} Claim failed.".format(
                        e.__class__.__name__, e))

    def claim(self):
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

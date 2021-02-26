import asyncio
from pyppeteer import launch, launcher
import time
from getpass import getpass
import schedule


class epic_claimer:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.browser = loop.run_until_complete(
            launch(options={"args": ["--no-sandbox"], "headless": False}, userDataDir="userdata")
        )
        self.page = loop.run_until_complete(self.browser.pages())[0]

    def close(self):
        asyncio.get_event_loop().run_until_complete(self.browser.close())

    async def await_type(self, selector, text, sleep_time=0):
        await self.page.waitForSelector(selector)
        time.sleep(sleep_time)
        await self.page.type(selector, text)

    async def await_click(self, selector, sleep_time=2):
        await self.page.waitForSelector(selector)
        time.sleep(sleep_time)
        await self.page.click(selector)
    
    async def await_get_text(self, selector, property="textContent"):
        await self.page.waitForSelector(selector)
        return await (await (await self.page.querySelector(selector)).getProperty(property)).jsonValue()
    
    async def await_detect(self, selector, timeout=None):
        try:
            if timeout != None:
                await self.page.waitForSelector(selector, options={"timeout": timeout})
            else:
                await self.page.waitForSelector(selector)
            return True
        except:
            return False
    
    async def await_try_click(self, selector, sleep_time=2):
        if await self.await_detect(selector):
            time.sleep(sleep_time)
            await self.await_click(selector)
            return True
        return False

    async def login(self):
        await self.page.goto("https://www.epicgames.com/", options={"timeout": 120000})
        if (await self.await_get_text("#user > ul > li > a", "href")) == "https://www.epicgames.com/login":
            for i in range(0, 5):
                try:
                    email = input("Email: ")
                    password = getpass("Password: ")
                    await self.await_click("#user")
                    await self.await_click("#login-with-epic")
                    await self.await_type("#email", email)
                    await self.await_type("#password", password)
                    await self.await_click("#sign-in[tabindex=\"0\"]")
                    if await self.await_detect("#code", 120000):
                        await self.await_type("#code", input("2FA code: "))
                        await self.await_click("#continue[tabindex=\"0\"]")
                    await self.page.waitForSelector("#user")
                    break
                except Exception as e:
                    log("{}: {}".format(e.__class__.__name__, e))
                    log("Login failed.")
                    if i < 4:
                        log("Retrying...")
                    else:
                        exit()
            log("Login successed.")
            log("Now you can leave by pressing Ctrl + P + Q.")
    
    async def claim(self):
        await self.page.goto("https://www.epicgames.com/store/zh-CN/free-games",
            options={"timeout": 120000}
        )
        await self.page.waitForSelector("div[data-component=CustomDiscoverModules] > div:nth-child(2) " \
            "div[data-component=CardGridDesktopBase"
        )
        item_list = await self.page.querySelectorAll("div[data-component=CustomDiscoverModules] > " \
            "div:nth-child(2) div[class*=CardGridDesktopLandscape__cardWrapperDesktop]"
        )
        for index in range(0, len(item_list)):
            await self.page.waitForSelector("div[data-component=CustomDiscoverModules] > div:nth-child(2) " \
                "div[data-component=CardGridDesktopBase"
            )
            item = (await self.page.querySelectorAll("div[data-component=CustomDiscoverModules] > " \
                "div:nth-child(2) div[class*=CardGridDesktopLandscape__cardWrapperDesktop]")
            )[index]
            await item.click()
            await self.await_try_click("div[class*=WarningLayout__layout] Button")
            if await self.await_try_click("button[data-testid=purchase-cta-button]:not([disabled]):nth-child(1)"):
                if await self.await_try_click("#purchase-app > div > div.order-summary-container " \
                    "> div.order-summary-card > div.order-summary-card-inner " \
                    "> div.order-summary-content > div > div > button:not([disabled])"
                ):
                    await self.page.waitForSelector("div[class*=DownloadLogoAndTitle__header]")
                    log("Claim successed.")
            elif await self.await_try_click("button[data-testid=purchase-cta-button]:not([disabled]):nth-child(2)"):
                if await self.await_try_click("#purchase-app > div > div.order-summary-container " \
                    "> div.order-summary-card > div.order-summary-card-inner " \
                    "> div.order-summary-content > div > div > button:not([disabled])"
                ):
                    await self.page.waitForSelector("div[class*=DownloadLogoAndTitle__header]")
                    log("Claim successed.")
            await self.page.goto("https://www.epicgames.com/store/zh-CN/free-games",
                options={"timeout": 120000}
            )


def log(text):
    localtime = time.asctime(time.localtime(time.time()))
    print("[{}] {}".format(localtime, text))


if __name__ == "__main__":
    launcher.DEFAULT_ARGS.remove("--enable-automation")

    def job():
        try:
            claimer = epic_claimer()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(claimer.login())
            log("Claim start.")
            loop.run_until_complete(claimer.claim())
        except Exception as e:
            log("{}: {}".format( e.__class__.__name__, e))
        finally:
            claimer.close()
            log("Claim end.")

    job()

    schedule.every().day.at("09:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
import asyncio
from typing import List, Union
from pyppeteer import launch, launcher
import time
from getpass import getpass
from pyppeteer.element_handle import ElementHandle
import schedule
import os
import shutil


def log(text: str, level: str = "message") -> None:
    localtime = time.asctime(time.localtime(time.time()))
    if level == "message":
        print("[{}] {}".format(localtime, text))
    elif level == "warning":
        print("[{}] \033[33mWarning: {}\033[0m".format(localtime, text))
    elif level == "error":
        print("[{}] \033[31mError: {}\033[0m".format(localtime, text))


class epicgames_claimer:
    def __init__(self, data_dir: str = "User Data/Default") -> None:
        self.loop = asyncio.get_event_loop()
        self.browser = self.loop.run_until_complete(launch(options={"args": ["--no-sandbox"], "headless": False}, userDataDir=data_dir))
        self.page = self.loop.run_until_complete(self.browser.pages())[0]

    def close(self) -> None:
        self.loop.run_until_complete(self.browser.close())
        # 等待文件解除占用
        time.sleep(2)

    async def type_async(self, selector: str, text: str, sleep_time: Union[int, float] = 0) -> None:
        await self.page.waitForSelector(selector)
        await asyncio.sleep(sleep_time)
        await self.page.type(selector, text)

    async def click_async(self, selector: str, sleep_time: Union[int, float] = 2) -> None:
        await self.page.waitForSelector(selector)
        await asyncio.sleep(sleep_time)
        await self.page.click(selector)

    async def get_text_async(self, selector: str) -> str:
        await self.page.waitForSelector(selector)
        return await (await (await self.page.querySelector(selector)).getProperty("textContent")).jsonValue()

    async def get_texts_async(self, selector: str) -> List[str]:
        texts = []
        try:
            await self.page.waitForSelector(selector)
            for element in await self.page.querySelectorAll(selector):
                texts.append(await (await element.getProperty("textContent")).jsonValue())
        except:
            pass
        return texts

    async def get_element_text_async(self, element: ElementHandle) -> str:
        return await (await element.getProperty("textContent")).jsonValue()

    async def get_property_async(self, selector: str, property: str) -> str:
        await self.page.waitForSelector(selector)
        return await self.page.evaluate("document.querySelector('{}').getAttribute('{}')".format(selector, property))

    async def get_links_async(self, selector: str, filter_selector: str, filter_value: str) -> List[str]:
        links = []
        try:
            await self.page.waitForSelector(selector)
            elements = await self.page.querySelectorAll(selector)
            judgement_texts = await self.get_texts_async(filter_selector)
        except:
            pass
        for element, judgement_text in zip(elements, judgement_texts):
            if judgement_text == filter_value:
                link = await (await element.getProperty("href")).jsonValue()
                links.append(link)
        return links

    async def detect_async(self, selector: str, timeout: Union[int, None] = None) -> str:
        try:
            if timeout != None:
                await self.page.waitForSelector(selector, options={"timeout": timeout})
            else:
                await self.page.waitForSelector(selector)
            return True
        except:
            return False

    async def try_click_async(self, selector: str, sleep_time: Union[int, float] = 2) -> bool:
        try:
            await asyncio.sleep(sleep_time)
            await self.page.click(selector)
            return True
        except:
            return False

    async def get_elements_async(self, selector: str) -> Union[List[ElementHandle], None]:
        try:
            await self.page.waitForSelector(selector)
            return await self.page.querySelectorAll(selector)
        except:
            return None

    async def wait_for_element_text_change_async(self, element: ElementHandle, text: str, timeout: int = 30) -> None:
        if await self.get_element_text_async(element) != text:
            return
        for i in range(timeout):
            await asyncio.sleep(1)
            if await self.get_element_text_async(element) != text:
                return
        raise TimeoutError("Waiting for element \"{}\" text content change failed: timeout {}s exceeds".format(element, timeout))

    async def login_async(self, email: str) -> None:
        if email == None or email == "":
            raise ValueError("Email can't be null.")
        await self.page.goto("https://www.epicgames.com/store/en-US/", options={"timeout": 120000})
        if (await self.get_property_async("#user", "data-component")) == "SignedIn":
            return
        await self.click_async("#user")
        await self.click_async("#login-with-epic")
        await self.type_async("#email", email)
        await self.type_async("#password", getpass("Password: "))
        await self.click_async("#sign-in[tabindex='0']")
        if await self.detect_async("#code"):
            await self.type_async("#code", input("2FA code: "))
            await self.click_async("#continue[tabindex='0']")
        await self.page.waitForSelector("#user")

    def login(self, email: str) -> None:
        return self.loop.run_until_complete(self.login_async(email))

    def is_loggedin(self) -> bool:
        async def is_loggedin_async() -> bool:
            await self.page.goto("https://www.epicgames.com/store/en-US/", options={"timeout": 120000})
            if (await self.get_property_async("#user", "data-component")) == "SignedIn":
                return True
            else:
                return False
        return self.loop.run_until_complete(is_loggedin_async())

    async def claim_async(self, email: str = None) -> None:
        for i in range(0, 5):
            try:
                await self.page.goto("https://www.epicgames.com/store/en-US/free-games", options={"timeout": 120000})
                freegame_links = await self.get_links_async("div[data-component=CustomDiscoverModules] > "
                                                            "div:nth-child(2) "
                                                            "div[data-component=CardGridDesktopBase] a",
                                                            "div[data-component=CustomDiscoverModules] > "
                                                            "div:nth-child(2) div[data-component=CardGridDesktopBase] "
                                                            "div[data-component=StatusBar] span",
                                                            "Free Now")
                for link in freegame_links:
                    await self.page.goto(link, options={"timeout": 120000})
                    await self.try_click_async("div[class*=WarningLayout__layout] Button")
                    game_title = (await self.page.title())
                    get_buttons = await self.get_elements_async("button[data-testid=purchase-cta-button]")
                    for get_button in get_buttons:
                        await self.wait_for_element_text_change_async(get_button, "Loading")
                        if await self.get_element_text_async(get_button) == "Get":
                            await get_button.click()
                            await self.click_async("#purchase-app div.order-summary-content button:not([disabled])")
                            await self.page.waitForSelector("div[class*=DownloadLogoAndTitle__header]")
                            log("{}: \"{}\" has been claimed.".format(email, game_title))
                return
            except Exception as e:
                    log("{}: {}.".format(email, str(e).rstrip(".")), level="warning")
        log("Claim failed. Will retry next time.", level="error")

    def claim(self, email: str = None) -> None:
        self.loop.run_until_complete(self.claim_async(email))


class epicgames_claimer_manager():
    def __init__(self) -> None:
        launcher.DEFAULT_ARGS.remove("--enable-automation")
        try:
            os.mkdir("User Data")
        except:
            pass
        self.user_datas = os.listdir("User Data")
        if len(self.user_datas) == 0:
            while not self.add_account():
                pass
        else:
            self.choose_option()

    def add_account(self, email: str) -> None:
        if email == "":
            raise ValueError("Email cant't be null.")
        claimer = epicgames_claimer("User Data/{}".format(email))
        claimer.login(email)
        claimer.close()
        self.user_datas.append(email)

    def remove_account(self, email: str) -> None:
        if email == None:
            raise ValueError("Email can't be null.")
        shutil.rmtree("User Data/{}".format(email))
        self.user_datas.remove(email)

    def claim(self) -> None:
        for user in self.user_datas:
            claimer = epicgames_claimer("User Data/" + user)
            claimer.claim(user)
            claimer.close()

    def auto_remove_accounts(self) -> None:
        for user in self.user_datas:
            claimer = epicgames_claimer("User Data/" + user)
            if not claimer.is_loggedin():
                claimer.close()
                self.remove_account(user)
            else:
                claimer.close()

    def choose_option(self) -> None:
        while True:
            print("1. Add an account\n"
                  "2. Remove an account\n"
                  "3. List all accounts\n"
                  "4. Run the process")
            choice = input("Your choice: ")
            if choice == "1":
                try:
                    email = input("Email: ")
                    self.add_account(email)
                    log("\"{}\" has been added.")
                except Exception as e:
                    log("\"{}\" add failed. ({})".format(email, e))
            elif choice == "2":
                try:
                    email = input("which account you want to remove: ")
                    self.remove_account()
                    log("\"{}\" remove successed.".format(email))
                except Exception as e:
                    log("\"{}\" remove failed. ({})".format(email, e))
            elif choice == "3":
                print(self.user_datas)
            elif choice == "4":
                break
            print()

    def run(self) -> None:
        self.claim()
        schedule.every().day.at("09:00").do(self.claim)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    claimer = epicgames_claimer_manager()
    claimer.auto_remove_accounts()
    claimer.run()

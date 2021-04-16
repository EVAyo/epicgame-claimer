import asyncio
from typing import List, Union
from pyppeteer import launch, launcher
import time
from getpass import getpass
from pyppeteer.element_handle import ElementHandle
import schedule
import os
import shutil
import keyboard


class epicgames_claimer:
    def __init__(self, data_dir: str = "User Data/Default") -> None:
        self.loop = asyncio.get_event_loop()
        self.browser = self.loop.run_until_complete(
            launch(options={
                "args": ["--no-sandbox"],
                "headless": False
            },
                   userDataDir=data_dir))
        self.page = self.loop.run_until_complete(self.browser.pages())[0]

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
              func_try: callable,
              times: int,
              func_except: Union[callable, None] = None,
              func_finally: Union[callable, None] = None) -> None:
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
        await asyncio.sleep(sleep_time)
        await self.page.type(selector, text)

    async def click_async(self,
                          selector: str,
                          sleep_time: Union[int, float] = 2) -> None:
        await self.page.waitForSelector(selector)
        await asyncio.sleep(sleep_time)
        await self.page.click(selector)

    async def get_text_async(self, selector: str) -> str:
        await self.page.waitForSelector(selector)
        return await (await (await self.page.querySelector(selector)
                             ).getProperty("textContent")).jsonValue()

    async def get_texts_async(self, selector: str) -> List[str]:
        texts = []
        try:
            await self.page.waitForSelector(selector)
            for element in await self.page.querySelectorAll(selector):
                texts.append(await
                             (await
                              element.getProperty("textContent")).jsonValue())
        except:
            pass
        return texts

    async def get_element_text_async(self, element: ElementHandle) -> str:
        return await (await element.getProperty("textContent")).jsonValue()

    async def get_property_async(self, selector: str, property: str) -> str:
        await self.page.waitForSelector(selector)
        return await self.page.evaluate(
            "document.querySelector('{}').getAttribute('{}')".format(
                selector, property))

    async def get_links_async(self, selector: str, filter_selector: str,
                              filter_value: str) -> List[str]:
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
        try:
            await asyncio.sleep(sleep_time)
            await self.page.click(selector)
            return True
        except:
            return False

    async def get_elements_async(
            self, selector: str) -> Union[List[ElementHandle], None]:
        try:
            await self.page.waitForSelector(selector)
            return await self.page.querySelectorAll(selector)
        except:
            return None

    async def wait_for_element_text_change_async(self,
                                                 element: ElementHandle,
                                                 text: str,
                                                 timeout: int = 30) -> None:
        if await self.get_element_text_async(element) != text:
            return
        for i in range(timeout):
            await asyncio.sleep(1)
            if await self.get_element_text_async(element) != text:
                return
        raise TimeoutError(
            "Waiting for element \"{}\" text content change failed: timeout {}s exceeds"
            .format(element, timeout))

    async def login_async(self, email: str = None) -> bool:
        for i in range(0, 5):
            try:
                await self.page.goto("https://www.epicgames.com/store/en-US/",
                                     options={"timeout": 120000})
                if (await self.get_property_async(
                        "#user", "data-component")) == "SignedIn":
                    return True
                await self.click_async("#user")
                await self.click_async("#login-with-epic")
                if email == None:
                    email = input("Email: ")
                await self.type_async("#email", email)
                await self.type_async("#password", getpass("Password: "))
                await self.click_async("#sign-in[tabindex='0']")
                if await self.detect_async("#code"):
                    await self.type_async("#code", input("2FA code: "))
                    await self.click_async("#continue[tabindex='0']")
                await self.page.waitForSelector("#user")
                self.log("Login successed.")
                return True
            except Exception as e:
                if i < 4:
                    self.log("{}.".format(str(e).rstrip(".")), level="warning")
                else:
                    self.log(
                        "{}. Login failed. Will retry next time.".format(e),
                        level="error")
                    return False

    def login(self, email: str = None) -> bool:
        return self.loop.run_until_complete(self.login_async(email))

    async def login_noretry_async(self, email: str = None) -> bool:
        await self.page.goto("https://www.epicgames.com/store/en-US/",
                                options={"timeout": 120000})
        if (await self.get_property_async(
                "#user", "data-component")) == "SignedIn":
            return
        await self.click_async("#user")
        await self.click_async("#login-with-epic")
        if email == None:
            email = input("Email: ")
        await self.type_async("#email", email)
        await self.type_async("#password", getpass("Password: "))
        await self.click_async("#sign-in[tabindex='0']")
        if await self.detect_async("#code"):
            await self.type_async("#code", input("2FA code: "))
            await self.click_async("#continue[tabindex='0']")
        await self.page.waitForSelector("#user")
        self.log("Login successed.")

    def login_noretry(self, email: str = None) -> bool:
        return self.loop.run_until_complete(self.login_noretry_async(email))

    async def claim_async(self, email: str = None) -> None:
        for i in range(0, 5):
            try:
                await self.page.goto(
                    "https://www.epicgames.com/store/en-US/free-games",
                    options={"timeout": 120000})
                freegame_links = await self.get_links_async(
                    "div[data-component=CustomDiscoverModules] > "
                    "div:nth-child(2) "
                    "div[data-component=CardGridDesktopBase] a",
                    filter_selector=
                    "div[data-component=CustomDiscoverModules] > "
                    "div:nth-child(2) div[data-component=CardGridDesktopBase] "
                    "div[data-component=StatusBar] span",
                    filter_value="Free Now")
                for link in freegame_links:
                    await self.page.goto(link, options={"timeout": 120000})
                    await self.try_click_async(
                        "div[class*=WarningLayout__layout] Button")
                    game_title = (await self.page.title())
                    get_buttons = await self.get_elements_async(
                        "button[data-testid=purchase-cta-button]")
                    for get_button in get_buttons:
                        await self.wait_for_element_text_change_async(
                            get_button, "Loading")
                        if await self.get_element_text_async(get_button
                                                             ) == "Get":
                            await get_button.click()
                            await self.click_async(
                                "#purchase-app div.order-summary-content button:not([disabled])"
                            )
                            await self.page.waitForSelector(
                                "div[class*=DownloadLogoAndTitle__header]")
                            self.log(
                                "\"{}\": \"{}\" has been claimed.".format(email, game_title))
                return
            except Exception as e:
                if i < 4:
                    self.log("{}.".format(str(e).rstrip(".")), level="warning")
                else:
                    self.log(
                        "{}. Claim failed. Will retry next time.".format(e),
                        level="error")

    def claim(self, email: str = None) -> None:
        self.loop.run_until_complete(self.claim_async(email))


class epicgames_claimer_multiaccount():
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
            while True:
                print(
                    "1. Add an account\n"
                    "2. Remove an account\n"
                    "3. Run Process"
                )
                choice = input ("Your choice: ")
                if choice == "1":
                    self.add_account()
                elif choice == "2":
                    self.remove_account()
                elif choice == "3":
                    break

    def log(self, text: str, level: str = "message") -> None:
        localtime = time.asctime(time.localtime(time.time()))
        if level == "message":
            print("[{}] {}".format(localtime, text))
        elif level == "warning":
            print("[{}] \033[33mWarning: {}\033[0m".format(localtime, text))
        elif level == "error":
            print("[{}] \033[31mError: {}\033[0m".format(localtime, text))

    def input_int_until_success(self, message: str) -> int:
        while True:
            try:
                return int(input(message))
            except ValueError:
                pass

    def add_account(self) -> bool:
        try:
            email = input("Email: ")
            claimer = epicgames_claimer("User Data/{}".format(email))
            claimer.login_noretry(email)
            claimer.close()
            self.user_datas.append(email)
            return True
        except Exception as e:
            claimer.close()
            while True:
                try:
                    time.sleep(1)
                    shutil.rmtree("User Data/{}".format(email))
                    break
                except:
                    pass
            self.log("\"{}\" login failed. ({})".format(email, e))
            return False
    
    def remove_account(self) -> bool:
        try:
            print(self.user_datas)
            email = input("which account you want to remove: ")
            shutil.rmtree("User Data/{}".format(email))
            self.user_datas.remove(email)
            return True
        except:
            return False

    def claim(self) -> None:
        for user in self.user_datas:
            claimer = epicgames_claimer("User Data/" + user)
            claimer.claim(user)
            claimer.close()

    def run(self) -> None:
        schedule.every().day.at("09:00").do(self.claim)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    claimer = epicgames_claimer_multiaccount()
    claimer.claim()
    claimer.run()

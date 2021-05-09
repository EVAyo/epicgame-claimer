import asyncio
import os
import shutil
import time
from getpass import getpass
from typing import List, Union

import func_timeout
import schedule
from pyppeteer import launch, launcher
from pyppeteer.element_handle import ElementHandle


def log(text: str, level: str = "message") -> None:
    localtime = time.asctime(time.localtime(time.time()))
    if level == "message":
        print("[{}] {}".format(localtime, text))
    elif level == "warning":
        print("\033[33m[{}] Warning: {}\033[0m".format(localtime, text))
    elif level == "error":
        print("\033[31m[{}] Error: {}\033[0m".format(localtime, text))


class epicgames_claimer:
    def __init__(self, data_dir: str = "User Data/Default", headless: bool = False) -> None:
        launcher.DEFAULT_ARGS.remove("--enable-automation")
        self.data_dir = data_dir
        self.headless = headless
        self.loop = asyncio.get_event_loop()
        self.open_browser()

    # 都这样了还能检测出来，这headless模式看来是开不了了
    async def headless_stuff_async(self):
        await self.page.setViewport({"width": 1024, "height": 768})
        await self.page.evaluateOnNewDocument(
            "() => {"
                "Object.defineProperty(navigator, 'userAgent', {get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',});"
                "Object.defineProperty(navigator, 'appVersion', {get: () => '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56d',});"
                "Object.defineProperty(navigator, 'plugins', {get: () => [{'description': 'Portable Document Format', 'filename': 'internal-pdf-viewer', 'length': 1, 'name': 'Chrome PDF Plugin'}]});"
                "Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en'],});"
                "const originalQuery = window.navigator.permissions.query;"
                "window.navigator.permissions.query = (parameters) => (parameters.name === 'notifications' ? Promise.resolve({ state: Notification.permission }) : originalQuery(parameters));"
                "window.chrome = {};"
                "window.chrome.app = {'InstallState':'a', 'RunningState':'b', 'getDetails':'c', 'getIsInstalled':'d'};"
                "window.chrome.csi = function(){};"
                "window.chrome.loadTimes = function(){};"
                "window.chrome.runtime = function(){};"
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
                "Reflect.defineProperty(navigator.connection,'rtt', {get: () => 150, enumerable:true});"
            "}"
        )

    def close_browser(self) -> None:
        self.loop.run_until_complete(self.browser.close())
        # 等待文件解除占用
        time.sleep(2)
    
    def open_browser(self) -> None:
        self.browser = self.loop.run_until_complete(launch(options={"args": ["--no-sandbox"], "headless": self.headless}, userDataDir=self.data_dir))
        self.page = self.loop.run_until_complete(self.browser.pages())[0]
        if self.headless:
            self.loop.run_until_complete(self.headless_stuff_async())

    async def type_async(self, selector: str, text: str, sleep: Union[int, float] = 0) -> None:
        await self.page.waitForSelector(selector)
        await asyncio.sleep(sleep)
        await self.page.type(selector, text)

    async def click_async(self, selector: str, sleep: Union[int, float] = 2, frame_index: int = 0) -> None:
        if frame_index == 0:
            await self.page.waitForSelector(selector)
            await asyncio.sleep(sleep)
            await self.page.click(selector)
        else:
            await self.page.waitForSelector("iframe:nth-child({})".format(frame_index))
            frame = self.page.frames[frame_index]
            await frame.waitForSelector(selector)
            await asyncio.sleep(sleep)
            await frame.click(selector)

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

    async def try_click_async(self, selector: str, sleep: Union[int, float] = 2) -> bool:
        try:
            await asyncio.sleep(sleep)
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
        for _ in range(timeout):
            await asyncio.sleep(1)
            if await self.get_element_text_async(element) != text:
                return
        raise TimeoutError("Waiting for element \"{}\" text content change failed: timeout {}s exceeds".format(element, timeout))

    async def login_async(self, email: str, password: str) -> None:
        if email == None or email == "":
            raise ValueError("Email can't be null.")
        if not await self.is_loggedin_async():
            await self.click_async("#user")
            await self.click_async("#login-with-epic")
            await self.type_async("#email", email)
            await self.type_async("#password", password)
            await self.click_async("#sign-in[tabindex='0']")
            if await self.detect_async("#code"):
                await self.type_async("#code", input("2FA code: "))
                await self.click_async("#continue[tabindex='0']")
            await self.page.waitForSelector("#user")

    def login(self, email: str, password: str) -> None:
        return self.loop.run_until_complete(self.login_async(email, password))

    async def is_loggedin_async(self) -> bool:
        await self.page.goto("https://www.epicgames.com/store/en-US/", options={"timeout": 120000})
        if (await self.get_property_async("#user", "data-component")) == "SignedIn":
            return True
        else:
            return False

    def is_loggedin(self) -> bool:
        return self.loop.run_until_complete(self.is_loggedin_async())

    async def claim_async(self) -> List[str]:
        await self.page.goto("https://www.epicgames.com/store/en-US/free-games", options={"timeout": 120000})
        freegame_links = await self.get_links_async("div[data-component=CustomDiscoverModules] > "
                                                    "div:nth-child(2) "
                                                    "div[data-component=CardGridDesktopBase] a",
                                                    "div[data-component=CustomDiscoverModules] > "
                                                    "div:nth-child(2) div[data-component=CardGridDesktopBase] "
                                                    "div[data-component=StatusBar] span",
                                                    "Free Now")
        claimed_game_titles = []
        for link in freegame_links:
            is_claim_successed = False
            await self.page.goto(link, options={"timeout": 120000})
            await self.try_click_async("div[class*=WarningLayout__layout] Button")
            game_title = (await self.page.title()).split(" | ")[0]
            purchase_buttons = await self.get_elements_async("button[data-testid=purchase-cta-button]")
            for purchase_button in purchase_buttons:
                await self.wait_for_element_text_change_async(purchase_button, "Loading")
                if await self.get_element_text_async(purchase_button) == "Get":
                    await purchase_button.click()
                    await self.click_async("#purchase-app div.order-summary-container button.btn-primary:not([disabled])", frame_index=1)
                    await self.click_async("div.ReactModal__Content button[data-component=ModalCloseButton]")
                    is_claim_successed = True
            if is_claim_successed:
                claimed_game_titles.append(game_title)
        return claimed_game_titles

    def claim(self) -> List[str]:
        return self.loop.run_until_complete(self.claim_async())
    
    def run(self, run_time: str) -> None:
        def logged_claim() -> None:
            for _ in range(0, 5):
                try:
                    claimed_game_titles = self.claim()
                    if len(claimed_game_titles) > 0:
                        log("{} has been claimed.".format(claimed_game_titles))
                    return
                except Exception as e:
                    log("{}.".format(str(e).rstrip(".")), level="warning")
            log("Claim failed. Will retry next time.", level="error")
        def everyday_job() -> None:
            self.open_browser()
            logged_claim()
            self.close_browser()
        logged_claim()
        self.close_browser()
        schedule.every().day.at(run_time).do(everyday_job)
        while True:
            schedule.run_pending()
            time.sleep(1)


class epicgames_claimer_manager():
    def __init__(self) -> None:
        launcher.DEFAULT_ARGS.remove("--enable-automation")
        try:
            os.mkdir("User Data")
        except:
            pass
        self.user_datas = os.listdir("User Data")
        if len(self.user_datas) == 0:
            while True:
                try:
                    email = input("Email: ")
                    self.add_account(email)
                    log("{} has been added.".format(email))
                    break
                except Exception as e:
                    log("{} add failed. ({})".format(email, e))
        else:
            try:
                while not self.choose_option():
                    print()
            except func_timeout.exceptions.FunctionTimedOut:
                print()

    def add_account(self, email: str) -> None:
        if email == None or email == "":
            raise ValueError("Email cant't be null.")
        claimer = epicgames_claimer("User Data/{}".format(email))
        claimer.login(email)
        claimer.close_browser()
        self.user_datas.append(email)

    def remove_account(self, email: str) -> None:
        if email == None or email == "":
            raise ValueError("Email can't be null.")
        shutil.rmtree("User Data/{}".format(email))
        self.user_datas.remove(email)

    def claim(self) -> None:
        for user in self.user_datas:
            claimer = epicgames_claimer("User Data/" + user)
            claimer.claim(user)
            claimer.close_browser()

    def auto_remove_accounts(self) -> None:
        for user in self.user_datas:
            claimer = epicgames_claimer("User Data/" + user)
            if not claimer.is_loggedin():
                claimer.close_browser()
                self.remove_account(user)
            else:
                claimer.close_browser()

    @func_timeout.func_set_timeout(600)
    def choose_option(self) -> bool:
        print("1. Add an account\n"
              "2. Remove an account\n"
              "3. List all accounts\n"
              "4. Run the process\n")
        choice = input("Your choice(Wait 10 minutes): ")
        if choice == "1":
            try:
                email = input("Email: ")
                self.add_account(email)
                log("{} has been added.".format(email))
            except Exception as e:
                log("{} add failed. ({})".format(email, e))
            return False
        elif choice == "2":
            try:
                email = input("which account you want to remove: ")
                self.remove_account()
                log("{} remove successed.".format(email))
            except Exception as e:
                log("{} remove failed. ({})".format(email, e))
            return False
        elif choice == "3":
            print(self.user_datas)
            return False
        elif choice == "4":
            return True

    def run(self) -> None:
        self.claim()
        schedule.every().day.at("09:00").do(self.claim)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    # claimer = epicgames_claimer_manager()
    # log("Claim has started.")
    # claimer.auto_remove_accounts()
    # claimer.run()
    claimer = epicgames_claimer(headless=False)
    def logged_login() -> None:
        for _ in range(5):
            try:
                if not claimer.is_loggedin():
                    email = input("Email: ")
                    password = getpass("Password: ")
                    claimer.login(email, password)
                    log("Login successed.")
                return
            except Exception as e:
                log("Login failed({}).".format(e), "warning")
                if claimer.headless:
                    claimer.loop.run_until_complete(claimer.page.screenshot({"path": "login.png"}))
        log("Login failed.", "error")
        time.sleep(8)
        exit()
    logged_login()
    log("Claim has started.")
    claimer.run("09:00")

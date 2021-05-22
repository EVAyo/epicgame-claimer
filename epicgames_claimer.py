import asyncio
import os
import time
from getpass import getpass
from typing import List, Union

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
    def __init__(self, data_dir: str = "User_Data/Default", headless: bool = False) -> None:
        launcher.DEFAULT_ARGS.remove("--enable-automation")
        self.data_dir = data_dir
        self.headless = headless
        self.loop = asyncio.get_event_loop()
        self.open_browser()

    # Useless.
    async def headless_stuff_async(self):
        await self.page.evaluateOnNewDocument(
            "() => {"
                "Object.defineProperty(navigator, 'userAgent', {get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',});"
                "Object.defineProperty(navigator, 'appVersion', {get: () => '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56d',});"
                "Object.defineProperty(navigator, 'plugins', {get: () => [{'description': 'Portable Document Format', 'filename': 'internal-pdf-viewer', 'length': 1, 'name': 'Chrome PDF Plugin'}]});"
                "Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en'],});"
                "const originalQuery = window.navigator.permissions.query;"
                "window.navigator.permissions.query = (parameters) => (parameters.name === 'notifications' ? Promise.resolve({ state: Notification.permission }) : originalQuery(parameters));"
                "window.chrome = {}; window.chrome.app = {'InstallState':'a', 'RunningState':'b', 'getDetails':'c', 'getIsInstalled':'d'}; window.chrome.csi = function(){}; window.chrome.loadTimes = function(){}; window.chrome.runtime = function(){};"
                "const newProto = navigator.__proto__; delete newProto.webdriver; navigator.__proto__ = newProto;"
                "Reflect.defineProperty(navigator.connection,'rtt', {get: () => 150, enumerable:true});"
                "const getParameter = WebGLRenderingContext.getParameter; WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'Intel Open Source Technology Center';}; if (parameter === 37446) {return 'Mesa DRI Intel(R) Ivybridge Mobile ';}; return getParameter(parameter);};"
                "['height', 'width'].forEach(property => {const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property); Object.defineProperty(HTMLImageElement.prototype, property, {...imageDescriptor, get: function() {if (this.complete && this.naturalHeight == 0) {return 16;}; return imageDescriptor.get.apply(this);},});});"
            "}"
        )

    def close_browser(self) -> None:
        self.loop.run_until_complete(self.browser.close())
        # 等待文件解除占用
        time.sleep(2)
    
    def open_browser(self) -> None:
        chromium_path = ""
        if os.path.exists("chromium"):
            chromium_path = "chromium/chrome.exe"
        else:
            chromium_path = launcher.executablePath()
        self.browser = self.loop.run_until_complete(launch(
            options={
                "args": ["--no-sandbox", "--disable-infobars", "--blink-settings=imagesEnabled=false"], 
                "headless": self.headless
            }, 
            userDataDir=self.data_dir, 
            executablePath=chromium_path
        ))
        self.page = self.loop.run_until_complete(self.browser.pages())[0]
        self.loop.run_until_complete(self.page.setViewport({"width": 1000, "height": 600}))
        if self.headless:
            self.loop.run_until_complete(self.headless_stuff_async())

    async def type_async(self, selector: str, text: str, sleep: Union[int, float] = 0) -> None:
        await self.page.waitForSelector(selector)
        await asyncio.sleep(sleep)
        await self.page.type(selector, text)

    async def click_async(self, selector: str, sleep: Union[int, float] = 2, timeout: int = 30000, frame_index: int = 0) -> None:
        if frame_index == 0:
            await self.page.waitForSelector(selector, options={"timeout": timeout})
            await asyncio.sleep(sleep)
            await self.page.click(selector)
        else:
            await self.page.waitForSelector("iframe:nth-child({})".format(frame_index), options={"timeout": timeout})
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
            return []
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

    async def login_async(self, email: str, password: str, two_fa_enabled: bool = True) -> None:
        if email == None or email == "":
            raise ValueError("Email can't be null.")
        if self.page.url != "https://www.epicgames.com/store/en-US/":
            await self.page.goto("https://www.epicgames.com/store/en-US/")
        await self.click_async("#user", timeout=120000)
        await self.click_async("#login-with-epic", timeout=120000)
        await self.type_async("#email", email)
        await self.type_async("#password", password)
        await self.click_async("#sign-in[tabindex='0']", timeout=120000)
        if two_fa_enabled:
            if await self.detect_async("#code", timeout=120000):
                await self.type_async("#code", input("2FA code: "))
                await self.click_async("#continue[tabindex='0']", timeout=120000)
        await self.page.waitForSelector("#user", timeout=120000)

    def login(self, email: str, password: str, two_fa_enabled: bool = True) -> None:
        return self.loop.run_until_complete(self.login_async(email, password, two_fa_enabled))

    async def is_loggedin_async(self) -> bool:
        await self.page.goto("https://www.epicgames.com/store/en-US/", options={"timeout": 120000})
        if (await self.get_property_async("#user", "data-component")) == "SignedIn":
            return True
        else:
            return False

    def is_loggedin(self) -> bool:
        return self.loop.run_until_complete(self.is_loggedin_async())
    
    async def get_freegame_links_async(self) -> List[str]:
        if self.page.url != "https://www.epicgames.com/store/en-US/free-games":
            await self.page.goto("https://www.epicgames.com/store/en-US/free-games")
        await self.page.waitForSelector("div[data-component=OfferCard]")
        freegame_links = []
        freegame_links_len = len(await self.page.querySelectorAll("div[data-component=OfferCard]"))
        for freegame_index in range(freegame_links_len):
            freegame_link = await self.page.evaluate("document.querySelectorAll('div[data-component=OfferCard]')[{}].parentElement.href".format(freegame_index))
            if freegame_link != "https://www.epicgames.com/store/en-US/free-games":
                freegame_links.append(freegame_link)
        return freegame_links
        
    async def claim_async(self) -> List[str]:
        await self.page.goto("https://www.epicgames.com/store/en-US/free-games", options={"timeout": 480000})
        freegame_links = await self.get_freegame_links_async()
        claimed_game_titles = []
        for link in freegame_links:
            is_claim_successed = False
            await self.page.goto(link, options={"timeout": 480000})
            await self.try_click_async("div[class*=WarningLayout__layout] Button")
            game_title = (await self.page.title()).split(" | ")[0]
            purchase_buttons = await self.get_elements_async("button[data-testid=purchase-cta-button]")
            for purchase_button in purchase_buttons:
                await self.wait_for_element_text_change_async(purchase_button, "Loading")
                if await self.get_element_text_async(purchase_button) == "Get":
                    await purchase_button.click()
                    await self.try_click_async("div[data-component=platformUnsupportedWarning] > Button")
                    await self.click_async("#purchase-app div.order-summary-container button.btn-primary:not([disabled])", frame_index=1)
                    await self.click_async("div.ReactModal__Content button[data-component=ModalCloseButton]")
                    is_claim_successed = True
            if is_claim_successed:
                claimed_game_titles.append(game_title)
        return claimed_game_titles

    def claim(self) -> List[str]:
        return self.loop.run_until_complete(self.claim_async())

    def logged_login(self) -> bool:
        for _ in range(5):
            try:
                if not self.is_loggedin():
                    email = input("Email: ")
                    password = getpass("Password: ")
                    self.login(email, password)
                    log("Login successed.")
                return True
            except Exception as e:
                log("Login failed({}).".format(e), "warning")
                if self.headless:
                    self.loop.run_until_complete(self.page.screenshot({"path": "login.png"}))
        log("Login failed.", "error")
        return False
    
    def logged_claim(self) -> None:
        for _ in range(0, 5):
            try:
                claimed_game_titles = self.claim()
                if len(claimed_game_titles) > 0:
                    log("{} has been claimed.".format(str(claimed_game_titles).strip("[]").replace("'", "")))
                return
            except Exception as e:
                log("{}.".format(str(e).rstrip(".")), level="warning")
        log("Claim failed. Will retry next time.", level="error")

    def run(self, at: str) -> None:
        def everyday_job() -> None:
            self.open_browser()
            self.logged_claim()
            self.close_browser()
        self.logged_claim()
        self.close_browser()
        schedule.every().day.at(at).do(everyday_job)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    log("Claimer is starting...")
    claimer = epicgames_claimer(headless=False)
    if claimer.logged_login():
        log("Claim has started.")
        claimer.run("09:00")
    else:
        time.sleep(8)
        exit(1)

import argparse
import asyncio
import os
import signal
import time
from getpass import getpass
from typing import List, Union

from pyppeteer import launch, launcher
from pyppeteer.element_handle import ElementHandle


class epicgames_claimer:
    def __init__(self, data_dir: str = "User_Data/Default", headless: bool = False, sandbox: bool = False, chromium_path: Union[str, None] = None) -> None:
        try:
            launcher.DEFAULT_ARGS.remove("--enable-automation")
        except ValueError:
            pass
        self.data_dir = data_dir
        self.headless = headless
        self.sandbox = sandbox
        self.chromium_path = chromium_path
        self._loop = asyncio.get_event_loop()
        self.open_browser()
    
    @staticmethod
    def log(text: str, level: str = "info") -> None:
        localtime = time.asctime(time.localtime(time.time()))
        if level == "info":
            print("[{}] {}".format(localtime, text))
        elif level == "warning":
            print("\033[33m[{}] Warning: {}\033[0m".format(localtime, text))
        elif level == "error":
            print("\033[31m[{}] Error: {}\033[0m".format(localtime, text))

    async def _headless_stealth_async(self):
        await self.page.evaluateOnNewDocument(
            "() => {"
                "Object.defineProperty(navigator, 'appVersion', {get: () => '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36',});"
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
        await self.page.evaluateOnNewDocument("window.navigator.chrome = {runtime: {}, loadTimes: function() {}, csi: function() {}, app: {}};")
        await self.page.evaluateOnNewDocument("window.navigator.language = {runtime: {}, loadTimes: function() {}, csi: function() {}, app: {}};")
        await self.page.setExtraHTTPHeaders({"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"})
        await self.page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36")

    def close_browser(self) -> None:
        self._loop.run_until_complete(self.browser.close())
    
    async def _open_browser_async(self) -> None:
        if self.chromium_path == None and os.path.exists("chrome-win32"):
            self.chromium_path = "chrome-win32/chrome.exe"
        browser_args = ["--disable-infobars", "--blink-settings=imagesEnabled=false"]
        if not self.sandbox:
            browser_args.append("--no-sandbox")
        self.browser = await launch(
            options={"args": browser_args, "headless": self.headless}, 
            userDataDir=self.data_dir, 
            executablePath=self.chromium_path
        )
        self.page = (await self.browser.pages())[0]
        await self.page.setViewport({"width": 1000, "height": 600})
        if self.headless:
            await self._headless_stealth_async()
    
    def open_browser(self) -> None:
        return self._loop.run_until_complete(self._open_browser_async())

    async def _type_async(self, selector: str, text: str, sleep: Union[int, float] = 0) -> None:
        await self.page.waitForSelector(selector)
        await asyncio.sleep(sleep)
        await self.page.type(selector, text)

    async def _click_async(self, selector: str, sleep: Union[int, float] = 2, timeout: int = 30000, frame_index: int = 0) -> None:
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

    async def _get_text_async(self, selector: str) -> str:
        await self.page.waitForSelector(selector)
        return await (await (await self.page.querySelector(selector)).getProperty("textContent")).jsonValue()

    async def _get_texts_async(self, selector: str) -> List[str]:
        texts = []
        try:
            await self.page.waitForSelector(selector)
            for element in await self.page.querySelectorAll(selector):
                texts.append(await (await element.getProperty("textContent")).jsonValue())
        except:
            pass
        return texts

    async def _get_element_text_async(self, element: ElementHandle) -> str:
        return await (await element.getProperty("textContent")).jsonValue()

    async def _get_property_async(self, selector: str, property: str) -> str:
        await self.page.waitForSelector(selector)
        return await self.page.evaluate("document.querySelector('{}').getAttribute('{}')".format(selector, property))

    async def _get_links_async(self, selector: str, filter_selector: str, filter_value: str) -> List[str]:
        links = []
        try:
            await self.page.waitForSelector(selector)
            elements = await self.page.querySelectorAll(selector)
            judgement_texts = await self._get_texts_async(filter_selector)
        except:
            return []
        for element, judgement_text in zip(elements, judgement_texts):
            if judgement_text == filter_value:
                link = await (await element.getProperty("href")).jsonValue()
                links.append(link)
        return links

    async def _find_async(self, selector: str, timeout: Union[int, None] = None) -> str:
        try:
            if timeout != None:
                await self.page.waitForSelector(selector, options={"timeout": timeout})
            else:
                await self.page.waitForSelector(selector)
            return True
        except:
            return False

    async def _try_click_async(self, selector: str, sleep: Union[int, float] = 2) -> bool:
        try:
            await asyncio.sleep(sleep)
            await self.page.click(selector)
            return True
        except:
            return False

    async def _get_elements_async(self, selector: str) -> Union[List[ElementHandle], None]:
        try:
            await self.page.waitForSelector(selector)
            return await self.page.querySelectorAll(selector)
        except:
            return None

    async def _wait_for_element_text_change_async(self, element: ElementHandle, text: str, timeout: int = 30) -> None:
        if await self._get_element_text_async(element) != text:
            return
        for _ in range(timeout):
            await asyncio.sleep(1)
            if await self._get_element_text_async(element) != text:
                return
        raise TimeoutError("Waiting for element \"{}\" text content change failed: timeout {}s exceeds".format(element, timeout))

    async def _navigate_async(self, url: str, timeout: int = 30000, reload: bool = True) -> None:
        if self.page.url == url and not reload:
            return
        await self.page.goto(url, options={"timeout": timeout})

    async def _close_autoplay_async(self):
        await self._navigate_async("https://www.epicgames.com/store/en-US/p/fortnite")
        await self._click_async("button[data-testid=settings-button]")
        if await self._find_async("#on[checked]", timeout=4000):
            await self._click_async("div[data-testid=settings-container] button")
            await asyncio.sleep(2)

    async def _login_async(self, email: str, password: str, two_fa_enabled: bool = True, remember_me: bool = True) -> None:
        if email == None or email == "":
            raise ValueError("Email can't be null.")
        if not await self._is_logged_in_async():
            await self._click_async("#user", timeout=120000)
            await self._click_async("#login-with-epic", timeout=120000)
            await self._type_async("#email", email)
            await self._type_async("#password", password)
            if not remember_me:
                await self._click_async("#rememberMe")
            await self._click_async("#sign-in[tabindex='0']", timeout=120000)
            if two_fa_enabled:
                await self.page.waitForNavigation(options={"timeout": 120000})
                if self.page.url != "https://www.epicgames.com/store/en-US/":
                    await self._type_async("input[name=code-input-0]", input("2FA code: "))
                    await self._click_async("#continue[tabindex='0']", timeout=120000)
            await self.page.waitForSelector("#user", timeout=120000)
            await self._close_autoplay_async()

    def login(self, email: str, password: str, two_fa_enabled: bool = True, remember_me: bool = True) -> None:
        return self._loop.run_until_complete(self._login_async(email, password, two_fa_enabled, remember_me))
    
    async def _is_logged_in_async(self) -> bool:
        await self._navigate_async("https://www.epicgames.com/store/en-US/", timeout=120000)
        if (await self._get_property_async("#user", "data-component")) == "SignedIn":
            return True
        else:
            return False

    def is_logged_in(self) -> bool:
        return self._loop.run_until_complete(self._is_logged_in_async())
    
    async def _get_free_game_links_async(self) -> List[str]:
        await self._navigate_async("https://www.epicgames.com/store/en-US/free-games")
        await self.page.waitForSelector("div[data-component=OfferCard]")
        freegame_links = []
        freegame_links_len = len(await self.page.querySelectorAll("div[data-component=OfferCard]"))
        freegame_statuses = await self._get_texts_async("div[data-component=OfferCard] div[data-component=StatusBar]")
        for freegame_index in range(freegame_links_len):
            freegame_status = freegame_statuses[freegame_index]
            freegame_link = await self.page.evaluate("document.querySelectorAll('div[data-component=OfferCard]')[{}].parentElement.href".format(freegame_index))
            if freegame_link != "https://www.epicgames.com/store/en-US/free-games" and freegame_status == "Free Now":
                freegame_links.append(freegame_link)
        return freegame_links
    
    def get_free_game_links(self) -> List[str]:
        return self._loop.run_until_complete(self._get_free_game_links_async())
        
    async def _claim_async(self) -> List[str]:
        await self._navigate_async("https://www.epicgames.com/store/en-US/free-games", timeout=480000)
        freegame_links = await self._get_free_game_links_async()
        claimed_game_titles = []
        for link in freegame_links:
            is_claim_successed = False
            await self._navigate_async(link, timeout=480000)
            await self._try_click_async("div[class*=WarningLayout__layout] Button")
            game_title = (await self.page.title()).split(" | ")[0]
            purchase_buttons_len = len(await self._get_elements_async("button[data-testid=purchase-cta-button]"))
            for purchase_button_index in range(purchase_buttons_len):
                purchase_button = (await self._get_elements_async("button[data-testid=purchase-cta-button]"))[purchase_button_index]
                await self._wait_for_element_text_change_async(purchase_button, "Loading")
                if await self._get_element_text_async(purchase_button) == "Get":
                    await purchase_button.click()
                    await self._try_click_async("#agree")
                    await self._try_click_async("div[class*=accept] Button")
                    await self._try_click_async("div[data-component=platformUnsupportedWarning] > Button")
                    await self._click_async("#purchase-app div.order-summary-container button.btn-primary:not([disabled])", frame_index=1)
                    await self._click_async("div.ReactModal__Content button[data-component=ModalCloseButton]", timeout=120000)
                    await self._navigate_async(link, timeout=480000, reload=True)
                    is_claim_successed = True
            if is_claim_successed:
                claimed_game_titles.append(game_title)
        return claimed_game_titles

    def claim(self) -> List[str]:
        return self._loop.run_until_complete(self._claim_async())

    def logged_login(self) -> bool:
        for _ in range(5):
            try:
                if not self.is_logged_in():
                    email = input("Email: ")
                    password = getpass("Password: ")
                    self.login(email, password)
                    self.log("Login successed. User data is saved at \"{}\".".format(self.data_dir))
                return True
            except Exception as e:
                self.log("Login failed({}).".format(e), "warning")
        self.log("Login failed.", "error")
        return False
    
    def logged_claim(self) -> None:
        for _ in range(0, 5):
            try:
                claimed_game_titles = self.claim()
                if len(claimed_game_titles) > 0:
                    self.log("{} has been claimed.".format(str(claimed_game_titles).strip("[]").replace("'", "")))
                return
            except Exception as e:
                self.log("{}.".format(str(e).rstrip(".")), level="warning")
        self.log("Claim failed.", level="error")

    def run(self, at: str = None, once: bool = False) -> None:
        import schedule
        signal.signal(signal.SIGINT, self._quit)
        signal.signal(signal.SIGTERM, self._quit)
        try:
            signal.signal(signal.SIGBREAK, self._quit)
        except AttributeError:
            pass
        try:
            signal.signal(signal.SIGHUP, self._quit)
        except AttributeError:
            pass
        def everyday_job() -> None:
            self.open_browser()
            self.logged_claim()
            self.close_browser()
        self.logged_claim()
        self.close_browser()
        if at == None or once:
            return
        schedule.every().day.at(at).do(everyday_job)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def _quit(self, signum = None, frame = None) -> None:
        try:
            self.close_browser()
        except:
            pass
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Claim weekly free games from Epic Games Store.",
        usage="python epicgames_claimer.py [-h] [-hf] [-c CHROMIUM_PATH] [-r RUN_AT] [-o]"
    )
    parser.add_argument("-hf", "--headful", action="store_true", help="run Chromium in headful mode")
    parser.add_argument("-c", "--chromium-path", type=str, help="set path to Chromium executable")
    parser.add_argument("-r", "--run-at", type=str, default="09:00", help="set daily check and claim time(HH:MM)")
    parser.add_argument("-o", "--once", action="store_true", help="claim once then exit")
    args = parser.parse_args()
    epicgames_claimer.log("Claimer is starting...")
    claimer = epicgames_claimer(headless=(not args.headful), chromium_path=args.chromium_path)
    if claimer.logged_login():
        epicgames_claimer.log("Claimer has started. Run at {} everyday.".format(args.run_at))
        claimer.run(args.run_at, once=args.once)
    else:
        exit(1)

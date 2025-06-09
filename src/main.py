from playwright.sync_api import sync_playwright, TimeoutError
from settings import settings
import random
import time


class TikTokViewer:

    def __init__(self) -> None:
        self.email = settings.TIKTOK_EMAIL
        self.password = settings.TIKTOK_PASS
        self.skip_percent = int(settings.SKIP_PERCENT)
        self.max_videos = int(settings.MAX_VIDEOS)
        self.search_query = settings.SEARCH_QUERY
        self.browser = None
        self.context = None
        self.page = None

    def _setup(self, headless: bool) -> None:
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=headless,
            slow_mo=1000,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--autoplay-policy=no-user-gesture-required",
                "--use-gl=egl",
            ],
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def _teardown(self):
        self.browser.close()

    def login(self) -> bool:
        """Авторизація в сервисі"""

        try:
            self.page.goto("https://www.tiktok.com/login", timeout=15000)
            self.page.click(
                'xpath=//*[@id="loginContainer"]/div/div/div/div[3]/div[2]',
                timeout=10000,
            )
            # авторизація через пошту
            self.page.locator('a[href="/login/phone-or-email/email"]').click(
                timeout=10000
            )

            # заповнення форми та імітація дій людини
            self.page.click('input[name="username"]')
            self.page.keyboard.type(self.email, delay=100)
            self.page.click('input[type="password"]')
            self.page.keyboard.type(self.password, delay=100)

            self.page.click('button[type="submit"]')
            self.page.wait_for_timeout(10000)
            print("[+] Успішна авторизація")
            return True
        except TimeoutError:
            print("[-] Помилка під час авторизації: сплив таймаут")
        return False

    def search(self) -> bool:
        """Пошук відео по запиту"""
        try:
            self.page.goto("https://www.tiktok.com", timeout=15000)
            self.page.get_by_role("searchbox").click(timeout=10000)

            self.page.locator("input.css-1ltjld2-InputElement.e14ntknm3").click()
            self.page.keyboard.type(self.search_query, delay=100)
            self.page.keyboard.press("Enter")
            self.page.wait_for_timeout(2000)
            print(f"[+] Результати пошуку: '{self.search_query}'")
            return True
        except TimeoutError:
            print("[-] Помилка пошуку: не вдалося завантажити результати")
        except Exception as e:
            print(f"[-] Помилка: {e}")
        return False

    def view_videos(self):
        """Перегляд відео з урахуванням skip_percent"""
        processed = 0
        while processed < self.max_videos:
            try:
                self.page.locator("div:has(a)").nth(0).click()
                self.page.evaluate("document.querySelector('video')?.play()")
                self.page.wait_for_timeout(5000)

                click_next = self.page.query_selector(
                    "button.css-1s9jpf8-ButtonBasicButtonContainer-StyledVideoSwitch e11s2kul10"
                )

                # elem = items[processed]
                # link = elem.get_attribute("href") or ""
                # vid_id = link.split("/")[-1].split("?")[0]

                # elem.click()
                # self.page.wait_for_selector("video", timeout=10000)
                # print(f"[~] Видео ID={vid_id} | {link}")

                # if random.randint(1, 100) <= self.skip_percent:
                #     print(f"[>] Пропущено видео: {vid_id}")
                # else:
                #     duration = self.page.evaluate(
                #         '() => document.querySelector("video").duration'
                #     )
                #     print(f"[+] Просмотр: {vid_id} ({duration:.2f}s)")
                #     time.sleep(duration)
                #
                # self.page.go_back()
                self.page.wait_for_timeout(2000)
                processed += 1
            except TimeoutError:
                print(f"[-] Не вдалося завантажити відео={vid_id}")
                processed += 1
            except Exception as e:
                print(f"[-] Помилка на відео={vid_id}: {e}")
                processed += 1

    def run(self, headless: bool = False) -> None:
        """Функція запуску

        :args bool headless: Запуск з графічним інтерфейсом або без
        """

        self._setup(headless)
        try:
            if not self.login():
                return
            if not self.search():
                return
            self.view_videos()
        finally:
            self._teardown()


def main() -> None:
    TikTokViewer().run()


if __name__ == "__main__":
    main()

from playwright.sync_api import sync_playwright, TimeoutError
from settings import settings
import random
import time


class TikTokViewer:
    """Клас-переглядач відео з Tik-Tok. Є авторизація та перегляд з параметрами skip_percent"""

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
        """Ініціалізація налаштувань браузера
        :args bool headless: Запуск з графічним інтерфейсом або без
        """
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            headless=headless,
            slow_mo=1000,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--autoplay-policy=no-user-gesture-required",
                "--use-gl=egl",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
            ],
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def _teardown(self) -> None:
        """Скидання всіх параметрів браузера та його закриття"""
        self.context.close()
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
            try:
                self.page.wait_for_selector(".captcha-verify-container", timeout=5000)
                print("[~] Пройдіть капчу для продовження...")
                self.page.wait_for_selector(
                    ".captcha-verify-container", state="detached", timeout=180000
                )
                print("[+] Капча пройдена!")
                self.page.wait_for_timeout(5000)
            except TimeoutError:
                print("[~] Капча не зʼявилася, продовжуємо.")
            print("[+] Успішна авторизація")
            return True
        except TimeoutError:
            print("[-] Помилка під час авторизації: сплив таймаут")
        return False

    def search(self) -> bool:
        """Пошук відео по запиту"""
        try:
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
        """Проглядає відео зі стрічки за результатами пошуку"""
        processed = 0

        # перше відео за запитом
        self.page.locator("div:has(a)").nth(0).click()

        while processed < self.max_videos:
            try:

                # отримуємо айді та посилання на відео
                video_url = self.page.url
                vid_id = video_url.split("/")[-1].split("?")[0]

                self.page.wait_for_function(
                    "document.querySelector('video') && document.querySelector('video').duration > 0",
                    timeout=10000,
                )

                # Отримуємо тривалість відео
                duration = self.page.evaluate(
                    "() => document.querySelector('video').duration"
                )

                # Вирішуємо чи треба скіпнути відео з урахуванням skip_percent
                if random.randint(1, 100) <= self.skip_percent:
                    print(f"[>] Пропущено відео: {vid_id} | {video_url}")
                    time.sleep(
                        random.randint(1, 3)
                    )  # імітація затримки на відео як у людини
                else:
                    print(
                        f"[+] Переглянуто відео: {vid_id} | {video_url} ({duration:.1f}с)"
                    )
                    time.sleep(duration)

                # Перехід до наступного відео
                self.page.locator('button[data-e2e="arrow-right"]').click(timeout=5000)

                processed += 1
                self.page.wait_for_timeout(1000)

            except TimeoutError:
                print("[-] Timeout при завантаженні відео")
                processed += 1
            except Exception as e:
                print(f"[-] Помилка при перегляді відео: {e}")
                processed += 1

    def run(self, headless: bool = False) -> None:
        """Функція запуску

        :args bool headless: Запуск з графічним інтерфейсом або без. За замовчуванням False
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

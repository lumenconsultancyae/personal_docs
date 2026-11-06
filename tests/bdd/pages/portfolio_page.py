import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

VIEWPORTS = {
    "desktop": (1440, 900),
    "tablet": (768, 1024),
    "mobile": (390, 844),
}


class PortfolioPage:
    """Driver-encapsulated Page Object for the Personal Portfolio application."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (
            base_url
            or os.environ.get("PORTFOLIO_BASE_URL", "http://host.docker.internal:3005")
        ).rstrip("/")
        opts = Options()
        opts.binary_location = os.environ.get("CHROMIUM_BIN", "/usr/bin/chromium")
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        chromedriver_path = os.environ.get("CHROMEDRIVER_BIN", "/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(
            service=Service(chromedriver_path), options=opts
        )
        self.wait = WebDriverWait(self.driver, 10)

    def quit(self) -> None:
        if self.driver:
            self.driver.quit()

    def set_viewport(self, name: str) -> None:
        width, height = VIEWPORTS[name.lower()]
        self.driver.set_window_size(width, height)
        time.sleep(0.2)

    def open_path(self, path: str = "/") -> None:
        url = f"{self.base_url}{path if path.startswith('/') else '/' + path}"
        self.driver.get(url)
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "main"))
        )

    def reset_storage_and_open(self, path: str = "/", viewport: str = "desktop") -> None:
        self.set_viewport(viewport)
        self.open_path("/")
        self.driver.execute_script("window.localStorage.clear();")
        self.open_path(path)
        self.wait_for_route_ready()

    def wait_for_route_ready(self) -> None:
        self.wait.until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "[data-testid='route-skeleton']")) == 0
        )

    def reload(self) -> None:
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
        self.wait_for_route_ready()

    def current_url(self) -> str:
        return self.driver.current_url

    def click_testid(self, testid: str) -> None:
        def _click(d: webdriver.Chrome) -> bool:
            el = d.find_element(By.CSS_SELECTOR, f"[data-testid='{testid}']")
            el.click()
            return True

        self.wait.until(_click)

    def fill_testid(self, testid: str, value: str) -> None:
        def _fill(d: webdriver.Chrome) -> bool:
            el = d.find_element(By.CSS_SELECTOR, f"[data-testid='{testid}']")
            el.clear()
            el.send_keys(value)
            return True

        self.wait.until(_fill)

    def select_by_testid(self, testid: str, value: str) -> None:
        def _select(d: webdriver.Chrome) -> bool:
            el = d.find_element(By.CSS_SELECTOR, f"[data-testid='{testid}']")
            Select(el).select_by_value(value)
            return True

        self.wait.until(_select)

    def is_visible_testid(self, testid: str) -> bool:
        els = self.driver.find_elements(
            By.CSS_SELECTOR, f"[data-testid='{testid}']"
        )
        return any(e.is_displayed() for e in els)

    def wait_for_testid(self, testid: str) -> str:
        el = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f"[data-testid='{testid}']")
            )
        )
        return el.text

    def wait_for_testid_gone(self, testid: str) -> None:
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, f"[data-testid='{testid}']")
            )
        )

    def get_table_text(self, testid: str = "projects-table-container") -> str:
        el = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f"[data-testid='{testid}']")
            )
        )
        return el.text

    def wait_for_url_contains(self, fragment: str) -> None:
        self.wait.until(lambda d: fragment in d.current_url)

    def has_bounded_scroll_container(
        self, testid: str = "projects-table-container"
    ) -> bool:
        el = self.driver.find_element(
            By.CSS_SELECTOR, f"[data-testid='{testid}']"
        )
        classes = el.get_attribute("class") or ""
        return "bounded-table-container" in classes

    def get_horizontal_overflow_delta(self) -> int:
        return int(
            self.driver.execute_script(
                "return document.documentElement.scrollWidth - window.innerWidth;"
            )
        )

    def get_severe_console_errors(self) -> list[str]:
        try:
            logs = self.driver.get_log("browser")
        except Exception:
            return []
        severe: list[str] = []
        for entry in logs:
            if entry.get("level") == "SEVERE":
                msg = str(entry.get("message", ""))
                if "favicon" not in msg:
                    severe.append(msg)
        return severe

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import platform
import json
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class TestPro360Login(unittest.TestCase):
    def setUp(self):
        # 設置Chrome選項
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 無頭模式，如果需要可以取消註釋
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-web-security')  # 禁用同源策略
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # 檢查是否為Apple Silicon
        is_arm = platform.processor() == 'arm'
        
        # 初始化WebDriver，針對M1/M2 Mac特別處理
        if is_arm:
            chrome_options.add_argument('--disable-gpu')
            chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
        # 從環境變數讀取配置
        self.base_url = os.getenv('BASE_URL', 'https://staging.pro360.com.tw')
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        
        # 檢查必要的環境變數是否存在
        if not self.email or not self.password:
            raise ValueError("請確保在 .env 文件中設置了 EMAIL 和 PASSWORD 環境變數")

    def wait_and_find_element(self, by, value, timeout=10):
        """等待並找到元素"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            print(f"無法找到元素 {value}: {str(e)}")
            return None

    def test_login_with_credentials(self):
        """測試使用帳號密碼登入"""
        try:
            # 訪問登入頁面
            self.driver.get(f"{self.base_url}/login")
            print("成功訪問登入頁面")

            # 等待頁面加載完成
            time.sleep(5)

            # 打印當前頁面中所有的input元素
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            print("\n找到的input元素:")
            for input_elem in inputs:
                try:
                    print(f"Type: {input_elem.get_attribute('type')}, Name: {input_elem.get_attribute('name')}, ID: {input_elem.get_attribute('id')}")
                except:
                    pass

            # 打印當前頁面中所有的button元素
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print("\n找到的button元素:")
            for button in buttons:
                try:
                    print(f"Text: {button.text}, Type: {button.get_attribute('type')}, Class: {button.get_attribute('class')}")
                except:
                    pass

            # 嘗試不同的選擇器來找到輸入框
            email_selectors = [
                "input[type='email']",
                "input[name='email']",
                "#email",
                "input[placeholder*='mail']",
                "input[placeholder*='郵件']"
            ]

            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "#password",
                "input[placeholder*='密碼']"
            ]

            # 尋找並填寫電子郵件
            email_input = None
            for selector in email_selectors:
                email_input = self.wait_and_find_element(By.CSS_SELECTOR, selector)
                if email_input:
                    print(f"找到電子郵件輸入框: {selector}")
                    break

            if not email_input:
                raise Exception("無法找到電子郵件輸入框")

            email_input.clear()
            email_input.send_keys(self.email)
            print("已輸入電子郵件")

            # 尋找並填寫密碼
            password_input = None
            for selector in password_selectors:
                password_input = self.wait_and_find_element(By.CSS_SELECTOR, selector)
                if password_input:
                    print(f"找到密碼輸入框: {selector}")
                    break

            if not password_input:
                raise Exception("無法找到密碼輸入框")

            password_input.clear()
            password_input.send_keys(self.password)
            print("已輸入密碼")

            # 嘗試不同的選擇器來找到登入按鈕
            button_selectors = [
                "button[type='submit']",
                "button.login-button",
                "button.submit-button",
                "button:contains('登入')",
                "input[type='submit']",
                ".btn-login",
                ".login-btn",
                "button.btn-primary"
            ]

            login_button = None
            for selector in button_selectors:
                try:
                    login_button = self.wait_and_find_element(By.CSS_SELECTOR, selector)
                    if login_button:
                        print(f"找到登入按鈕: {selector}")
                        break
                except:
                    continue

            if not login_button:
                # 如果無法通過CSS選擇器找到，嘗試通過按鈕文字找到
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    if "登入" in button.text:
                        login_button = button
                        print("通過文字內容找到登入按鈕")
                        break

            if not login_button:
                raise Exception("無法找到登入按鈕")

            # 點擊登入按鈕
            login_button.click()
            print("已點擊登入按鈕")

            # 等待登入完成並跳轉
            time.sleep(10)

            # 打印當前URL，用於確認登入狀態
            print(f"當前URL: {self.driver.current_url}")

            # 如果還在登入頁面，則登入失敗
            if "/login" in self.driver.current_url:
                # 獲取錯誤信息（如果有的話）
                try:
                    error_message = self.driver.find_element(By.CSS_SELECTOR, ".error-message").text
                    raise Exception(f"登入失敗：{error_message}")
                except:
                    raise Exception("登入失敗：未知原因")

            # 嘗試訪問個人資料頁面
            self.driver.get(f"{self.base_url}/dashboard")
            print("正在訪問個人資料頁面")
            time.sleep(5)

            # 再次確認URL，確保沒有被重定向到登入頁面
            if "/login" in self.driver.current_url:
                raise Exception("訪問個人資料頁面失敗：被重定向到登入頁面")

            # 打印頁面標題
            print(f"頁面標題: {self.driver.title}")

            # 獲取並打印localStorage中的token（如果有的話）
            storage = self.driver.execute_script("""
            let items = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                items[key] = localStorage.getItem(key);
            }
            return items;
            """)
            print("localStorage內容:", json.dumps(storage, indent=2))

            print("測試完成")

        except Exception as e:
            print(f"測試過程中發生錯誤: {str(e)}")
            # 如果發生錯誤，打印頁面源代碼以幫助調試
            print("\n頁面源代碼:")
            print(self.driver.page_source[:2000])
            raise

    def tearDown(self):
        # 關閉瀏覽器
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main() 
 
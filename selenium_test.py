from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# 配置 Chrome 选项
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920,1080')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--lang=zh-TW')


driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=chrome_options)


driver.get("https://www.google.com")

try:
    title = driver.title
    print("Success")
except Exception as e:
    print("Failed")
    print(str(e))
finally:
    driver.quit()
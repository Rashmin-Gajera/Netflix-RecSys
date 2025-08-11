
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def fetch_imdb_plot(imdb_url: str):
    opts = Options()
    opts.headless = True
    # path to chromedriver must be available in PATH
    with webdriver.Chrome(options=opts) as driver:
        driver.get(imdb_url)
        try:
            elem = driver.find_element(By.CSS_SELECTOR, '.ipc-html-content.ipc-html-content--base')
            return elem.text.strip()
        except Exception as e:
            return ""

if __name__ == "__main__":
    print(fetch_imdb_plot("https://www.imdb.com/title/tt1375666/"))

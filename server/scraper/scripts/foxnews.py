import requests
import time
import re
from datetime import date
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

# ===================================
# FOR DEPLOYING, UNCOMMENT LINE(s) BELOW
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# ===================================

# ===================================
# FOR DEPLOYING, UNCOMMENT LINE(s) BELOW
# chromeOptions = Options()
# chromeOptions.add_argument('--no-sandbox')
# chromeOptions.add_argument('--headless')
# chromeOptions.add_argument('--disable-dev-shm-usage')
# chromeOptions.add_argument('--log-path=chromedriver.log')
# chromeOptions.add_argument('--verbose')
# chromeOptions.add_argument('--disable-gpu')
# chromeOptions.add_argument("--window-size=1920,1080")
# ===================================

today = date.today().isoformat()


def scrape_foxnews():
    print("attempt fox news")
    try:
        # ===================================
        # FOR DEVELOPMENT, UNCOMMENT LINE BELOW
        driver = webdriver.Firefox()

        # ===================================
        # FOR DEPLOYING, UNCOMMENT LINE(s) BELOW
        # driver = webdriver.Chrome(
        #     executable_path="/home/pfteza/chromedriver", options=chromeOptions)
        # print("attempt start display")
        # display = Display(visible=0, size=(800, 600))
        # display.start()
        # print("successful start display")
        # ===================================
        print("attempt start driver")
        url = "https://www.foxnews.com/"
        driver.get(url)
        print("success start driver")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//main[@class='main-content']")))
        finally:
            innerHTML = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight-10000);var lenOfPage=document.body.scrollHeight;return document.body.innerHTML;")

            page_soup = BeautifulSoup(innerHTML, "html.parser")
            mainSection = page_soup.find("main", {"class": "main-content"})
            newsColumns = page_soup.find_all(
                "div", {"class": "collection-spotlight"})

            articlesList = []
            for column in newsColumns:
                articles = column.find_all("article")
                for article in articles:
                    try:
                        h2 = article.find("h2", {"class": "title"})
                        headline = h2.find("a")
                        link = headline["href"]
                        text = headline.get_text()

                        article_ = {
                            "site": "60721296a55796cad11d99e8",  # Hardcoded ObjectId
                            "headline": text,
                            "article_url": link,
                            "date": today
                        }

                        articlesList.append(article_)
                    except Exception as e:
                        print(f"error retrieving data: {e}")

            driver.quit()
            # ===================================
            # FOR DEPLOYING, UNCOMMENT LINE BELOW
            # display.stop()
            print("finish scrape cbs")
            return articlesList

    except Exception as e:
        print(f"error retrieving data: {e}")
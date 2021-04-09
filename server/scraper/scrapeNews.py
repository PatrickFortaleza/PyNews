import requests
import time
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# urls = [
#   "https://www.usatoday.com/",
#   "https://www.foxnews.com/",
#   "https://www.cnn.com/"
# ]


class Scrapeth():
    def __init__(self):
        self.__today = date.today().isoformat()
        self.__articles = []
        self.__driver = webdriver.Firefox()

        def scrape_cnn():
            try:
                url = "https://www.cnn.com/"
                self.__driver.get(url)
                try:
                    WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//section[@id='homepage1-zone-1']")))
                finally:
                    innerHTML = self.__driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight-10000);var lenOfPage=document.body.scrollHeight;return document.body.innerHTML;")

                    page_soup = BeautifulSoup(innerHTML, "html.parser")
                    topSection = page_soup.find(
                        "section", {"id": "homepage1-zone-1"})
                    newsColumns = topSection.find_all(
                        "div", {"class": "column"})

                    articlesList = []
                    for column in newsColumns[:3]:
                        articles = column.find_all("article")
                        for article in articles[:1]:
                            try:
                                h3 = article.find(
                                    "h3", {"class": "cd__headline"})
                                headline = h3.find("a")
                                link = headline["href"]
                                text = headline.get_text()

                                article_ = {
                                    "site": "6070628dbcdb9a31a261bb97",  # Hardcoded ObjectID
                                    "headline": text,
                                    "article_url": link,
                                    "date": self.__today
                                }

                                articlesList.append(article_)
                            except Exception as e:
                                print(f"error retrieving data: {e}")

                # Closes tab
                self.__driver.close()

                self.__articles = articlesList

            except Exception as e:
                self.__driver.close()
                print(f"error retrieving data: {e}")

        scrape_cnn()

# ----------------------------------------
# Getter setter for attributes
# ----------------------------------------
    @property
    def articles(self):
        return self.__articles

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re

class UpbitNoticeCrawler:
    def __init__(self, url="https://upbit.com/service_center/notice", keyword="거래지원 종료", filename="거래지원종료.txt"):
        self.url = url
        self.keyword = keyword
        self.filename = filename
        self.driver = None
        self.data = []
        self.existing_tickers = set()
        self.matched_tickers = set()

    def _init_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)

    def fetch_notices(self):
        self._init_driver()
        self.driver.get(self.url)
        time.sleep(5)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        notices = soup.select("table tbody tr a")
        self.driver.quit()

        for a in notices:
            title = a.get_text(strip=True)
            link = a.get("href")
            if title and link:
                self.data.append({
                    "title": title,
                    "link": "https://upbit.com" + link
                })

    def extract_tickers(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.existing_tickers = set(line.strip() for line in f.readlines())

        df = pd.DataFrame(self.data)

        for title in df["title"]:
            if self.keyword in title:
                match = re.search(r"\((.*?)\)", title)
                if match:
                    ticker = match.group(1).strip()
                    krw_ticker = f"KRW-{ticker}"
                    if krw_ticker not in self.existing_tickers:
                        self.matched_tickers.add(krw_ticker)

    def save_new_tickers(self):
        if self.matched_tickers:
            with open(self.filename, "a", encoding="utf-8") as f:
                for ticker in sorted(self.matched_tickers):
                    f.write(ticker + "\n")
            print(f"✅ 신규 저장된 티커: {sorted(self.matched_tickers)}")
        else:
            print("ℹ️ 신규 티커 없음. 기존과 동일합니다.")

    def run(self):
        self.fetch_notices()
        self.extract_tickers()
        self.save_new_tickers()

# 사용 예시
#if __name__ == "__main__":
#    crawler = UpbitNoticeCrawler()
#    crawler.run()

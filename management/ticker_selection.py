import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyupbit

class TickerManager:
    def __init__(self):
        self.past_completed_ticker = [
            'KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-SOL',
            'KRW-DOGE', 'KRW-ADA', 'KRW-TRX', 'KRW-LINK',
            'KRW-AVAX', 'KRW-SUI'
        ]
        self.now_ticker = []

    def fetch_web_tickers(self, url='https://coinmarketcap.com/ko/'):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(3)

        tickers = driver.find_elements(By.CLASS_NAME, 'coin-item-symbol')
        ticker_list = [ticker.text for ticker in tickers if ticker.text != '']

        driver.quit()
        return ticker_list

    def get_upbit_tickers(self):
        return pyupbit.get_tickers(fiat="KRW")

    def filter_tickers(self, web_tickers, upbit_tickers):
        now_ticker = [f'KRW-{ticker}' for ticker in web_tickers if f'KRW-{ticker}' in upbit_tickers]

        # 제외할 항목 제거
        for remove_ticker in ['KRW-USDT', 'KRW-USDC']:
            if remove_ticker in now_ticker:
                now_ticker.remove(remove_ticker)

        if len(now_ticker) < 10:
            raise ValueError("오류: ticker 수가 10 보다 작습니다.")

        return now_ticker[:10]

    def run(self):
        try:
            web_tickers = self.fetch_web_tickers()
            upbit_tickers = self.get_upbit_tickers()
            self.now_ticker = self.filter_tickers(web_tickers, upbit_tickers)

            print("성공!")
            print("현재 매매 티커:", self.now_ticker)

            self.past_completed_ticker = self.now_ticker
            print("과거 매매 티커:", self.past_completed_ticker)

        except Exception as e:
            self.now_ticker = self.past_completed_ticker
            print("티커 정보 조회 실패 - 이전 티커로 다시 매매 진행합니다.")
            print("현재 매매 티커:", self.now_ticker)


"""if __name__ == "__main__":
    manager = TickerManager()
    manager.run()"""
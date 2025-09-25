import pandas as pd
import math

class InvestmentAllocator:
    def __init__(self, ticker_list, trading_times, total_money):
        self.ticker_list = ticker_list
        self.trading_times = trading_times
        self.total_money = total_money
        self.per_slot_money = self._calculate_slot_money()
        self.records = []

    def _calculate_slot_money(self):
        total_slots = len(self.ticker_list) * len(self.trading_times)
        return int(self.total_money // total_slots)  # 소수점 버림, 정수

    def build_records(self):
        for ticker in self.ticker_list:
            entry = {
                "ticker": ticker,
                "trading_time": self.trading_times,
                "hoding_money": [self.per_slot_money] * len(self.trading_times),
                "hoding_coin": [0] * len(self.trading_times)  # float 아닌 int로도 가능
            }
            self.records.append(entry)

    def to_dataframe(self):
        return pd.DataFrame(self.records)

    def save_to_csv(self, filename="투자기록.csv"):
        df = self.to_dataframe()
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ CSV 저장 완료: {filename}")
        return df


def main():
    tickers = ['KRW-BTC', 'KRW-ETH']
    trading_times = [23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    total_money = 20000000

    # 클래스 초기화 및 실행
    allocator = InvestmentAllocator(tickers, trading_times, total_money)
    allocator.build_records()

    # ✅ DataFrame 객체로 받아서 외부에서 활용
    df = allocator.to_dataframe()

    # ✅ 필요시 저장도 가능
    allocator.save_to_csv("투자기록.csv")

    # ✅ DataFrame 사용 예시
    print(df.head())

if __name__ == "__main__":
    main()

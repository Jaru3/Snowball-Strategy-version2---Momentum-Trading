import pyupbit as pu
import pandas as pd
from datetime import datetime, timedelta
import os

class CryptoDataProcessor:
    def __init__(self, directory='coin_dataset'):
        self.directory = directory
        self._create_directory()

    def _create_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def fetch_and_save_data(self, ticker):
        print(ticker, "start")
        output_path = os.path.join(self.directory, f'{ticker}.csv')
        df = pu.get_ohlcv(ticker, interval="minute60", count=100000)
        df.to_csv(output_path)
        return output_path

    def preprocess_data(self, file_path):
        df = pd.read_csv(file_path)
        df.columns.values[0] = 'datetime'
        df['datetime'] = pd.to_datetime(df['datetime'])

        new_rows = []
        for i in range(1, len(df)):
            new_rows.append(df.iloc[i-1])
            time_diff = df['datetime'].iloc[i] - df['datetime'].iloc[i-1]
            if time_diff > timedelta(hours=1):
                missing_hours = int(time_diff.total_seconds() // 3600) - 1
                for h in range(1, missing_hours + 1):
                    new_row = df.iloc[i-1].copy()
                    new_row['datetime'] = df['datetime'].iloc[i-1] + timedelta(hours=h)
                    new_rows.append(new_row)
        new_rows.append(df.iloc[-1])

        new_df = pd.DataFrame(new_rows).reset_index(drop=True)
        new_df.to_csv(file_path, index=False)
        return df, new_df

    def analyze_data(self, df, new_df):
        for data, label in [(df, 'Original'), (new_df, 'Processed')]:
            df_dict = {}
            for i in range(len(data)):
                date = str(data['datetime'].iloc[i])[:10]
                df_dict[date] = df_dict.get(date, 0) + 1

            sorted_dict = sorted(df_dict.items(), key=lambda item: item[1])
            print(f"{label} Data Analysis:")
            print(sorted_dict[:10])
            print(f"{label} length: {len(data)}\n")

    def run(self):
        tickers = pu.get_tickers(fiat="KRW")
        for ticker in tickers:
            file_path = self.fetch_and_save_data(ticker)
            df, new_df = self.preprocess_data(file_path)
            self.analyze_data(df, new_df)

if __name__ == "__main__":
    processor = CryptoDataProcessor()
    processor.run()


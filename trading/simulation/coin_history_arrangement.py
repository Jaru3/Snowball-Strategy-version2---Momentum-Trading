import pyupbit as pu
import pandas as pd
from datetime import datetime, timedelta
import os

# 디렉토리 존재 여부 확인 후 생성
if not os.path.exists('coin_dataset'):
    os.makedirs('coin_dataset')

tickers = pu.get_tickers(fiat="KRW")

for ticker in tickers:
    print(ticker, " start")
    output_path = 'coin_dataset/' + str(ticker) + '.csv'
    df = pu.get_ohlcv(ticker, interval="minute60", count=100000)
    df.to_csv(output_path)
    df = pd.read_csv(output_path)
    df.columns.values[0] = 'datetime'
    df['datetime'] = pd.to_datetime(df['datetime'])

    # 시간 간격이 1시간이 아닌 부분을 찾아서 행 추가
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

    # 새로운 데이터프레임 생성
    new_df = pd.DataFrame(new_rows).reset_index(drop=True)

    # 변환된 데이터 저장
    new_df.to_csv(output_path, index=False)
    df_dict = {}
    for i in range(len(df)):
        if df["Unnamed: 0"][i][:10] in df_dict:
            df_dict[df["Unnamed: 0"][i][:10]]+=1
        else:
            df_dict[df["Unnamed: 0"][i][:10]]=1

    sorted_dict = sorted(df_dict.items(), key= lambda item:item[1], reverse=False)
    print(sorted_dict)
    print("전처리전 길이: ", len(df))
    print()
    
    df_dict = {}
    for i in range(len(new_df)):
        if new_df["Unnamed: 0"][i][:10] in df_dict:
            df_dict[new_df["Unnamed: 0"][i][:10]]+=1
        else:
            df_dict[new_df["Unnamed: 0"][i][:10]]=1

    sorted_dict = sorted(df_dict.items(), key= lambda item:item[1], reverse=False)
    print(sorted_dict)
    print("전처리후 길이: ", len(new_df))
    print()
    print()

import pyupbit
import pandas as pd
import numpy as np
import math
import time
import timeit
import pickle as pk
import smtplib # 메일을 보내기 위한 라이브러리 모듈
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

sender_email = "cwnms171@gmail.com"
app_password = "efuippuhknpgpxhy"  # 여기에 생성된 앱 비밀번호를 입력하세요

# 받는 사람의 이메일 주소
receiver_email = "cwnms171@gmail.com"

access_key = #공개키
secret_key = #비밀키

upbit = pyupbit.Upbit(access_key, secret_key)                               # line test X

error_num = [[0,0,0,0,0,0]] # 에러 발생(+1)후 다음번에는 초기화 0
money_share = [[1,1,1,1,1,1]]
coin_num = [[0.0,0.0,0.0,0.0,0.0,0.0]]
uuid=[['','','','','','']]
coin_tickers = ["KRW-BTC"]
times = [0,3,6,7,8,9,24]
time.sleep(115)

while True:

    print("\nstart\n")
    for i in range(6):
        start = timeit.default_timer()
        for j in range(len(coin_tickers)):
         #일일 거래 횟수
            """
            거래 방법 적기
            """
            #점검시 현재값 오류 예외처리하가(error_num +=1)
                                                # line test X
            df = pyupbit.get_ohlcv(coin_tickers[j],interval="minute60")                                # line test X
            price_pre24 = df['open'][175]
            price_now = pyupbit.get_current_price(coin_tickers[j]) 
            if price_now >= price_pre24 or price_now <= price_pre24*0.9:                          # line test X
                if money_share[j][i] == 0:
                    pass
                else:
                    now_balance = upbit.get_balance(coin_tickers[j])
                    buy_amount = int(upbit.get_balance("KRW")/np.sum(money_share))                  # line test X
                    buy_info = upbit.buy_limit_order(coin_tickers[j], price_now, math.floor((buy_amount/price_now)*10**8)/10**8)   
                    aft_balance = upbit.get_balance(coin_tickers[j])                                 # line test X
                    money_share[j][i] = 0
                    coin_num[j][i] = aft_balance-now_balance #구매한 만큼의 양(소수점 8자리 버림)          # line test X
                    #구매
                    """
                    여기서 고민 -> 해당 coin_balance 구하는 방법 생각하기 -> 실제 산거에서 소수점 8번쨰 자리까지 계산하는 법 생각하기
                    """

            else:
                if money_share[j][i] == 0:
                    sell_amount = coin_num[j][i]
                    sell_info = upbit.sell_limit_order(coin_tickers[j], price_now, sell_amount)
                    money_share[j][i] = 1
                    coin_num[j][i] = 0
                    #판매
                else:
                    pass

        # 결과 출력


        # 결과 메일로 보내기(백업)
        subject = "제목"+str(i)
        body = "이메일 내용입니다."+str(i)

        # MIMEText 객체 생성
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # 이메일 내용 추가
        message.attach(MIMEText(body, 'plain'))

        # Gmail SMTP 서버 설정
        smtp_server = "smtp.gmail.com"
        smtp_port = 465

        # SSL 연결 설정
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        # 로그인
        server.login(sender_email, app_password)

        # 이메일 전송
        server.sendmail(sender_email, receiver_email, message.as_string())

        # 연결 종료
        server.quit()


        print("\nfinish\n")

        stop = timeit.default_timer()

        # 0시,3시,6시,7시,8시,9시 실행
        time.sleep(3600*(times[i+1]-times[i]) - (stop - start))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 보내는 사람의 Gmail 계정 정보
sender_email = "cwnms171@gmail.com"
app_password = "efuippuhknpgpxhy"  # 여기에 생성된 앱 비밀번호를 입력하세요

# 받는 사람의 이메일 주소
receiver_email = "cwnms171@gmail.com"

# 이메일 제목과 내용
"""
error_num = [[0,0,0,0,0,0]] # 에러 발생(+1)후 다음번에는 초기화 0
money_share = [[1,1,1,1,1,1]]
coin_num = [[0.0,0.0,0.0,0.0,0.0,0.0]]
uuid=[['','','','','','']]
coin_tickers = ["KRW-BTC"]
times = [0,3,6,7,8,9,24]

for i in range(10):
    if i % 2 == 0:
        money_share[0][i%6] = 0
        coin_num[0][i%6] = 1

    if i % 2 == 1:
        money_share[0][i%6] = 1
        coin_num[0][i%6] = 0"""


def email_sender(ticker, time, sell, buy, money, coin):
    subject = str(time) + " : " + str(ticker) + "의 매매 결과 값입니다."
    if float(sell) > 0 and float(buy) == 0:
        body = str(ticker) + "를 매도 하였습니다.\n" \
            + "sell amount" + str(sell) + "\n" \
            + "money amount" + str(money)
    
    elif float(sell) == 0 and float(buy) > 0:
        body = str(ticker) + "를 매수 하였습니다.\n" \
            + "buy amount" + str(buy) + "\n" \
            + "coin amount" + str(coin)

    else:
        body = "매수매도에 오류가 발생하였습니다. 즉시 확인하길 바랍니다."
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
    print("이메일이 성공적으로 전송되었습니다.")
    return 0

email_sender("KRW-BTC", "2025-02-03-12H", "1234", "0", "1200000", "0")
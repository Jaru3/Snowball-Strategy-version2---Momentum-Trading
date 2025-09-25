import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class DateTimeInfo:
    def __init__(self):
        self.update()

    def update(self):
        """현재 날짜와 시간을 업데이트"""
        now = datetime.now()
        self.year = now.year
        self.month = now.month
        self.day = now.day
        self.hour = now.hour
        self.minute = now.minute
        self.second = now.second

    def get_datetime(self):
        """년-월-일-시간:00 형식으로 반환 (분을 00으로 고정)"""
        return f"{self.year}-{self.month:02d}-{self.day:02d}-{self.hour:02d}H"

class EmailSender:
    def __init__(self, sender_email, app_password, smtp_server="smtp.gmail.com", smtp_port=465):
        self.sender_email = sender_email
        self.app_password = app_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, receiver_email, ticker, time, sell, buy, money, coin):
        try:
            subject = f"{time} : {ticker}의 매매 결과 값입니다."
            
            if float(sell) > 0 and float(buy) == 0:
                body = (
                    f"{ticker}를 매도 하였습니다.\n"
                    f"sell amount: {sell}\n"
                    f"money amount: {money}"
                )
            elif float(sell) == 0 and float(buy) > 0:
                body = (
                    f"{ticker}를 매수 하였습니다.\n"
                    f"buy amount: {buy}\n"
                    f"coin amount: {coin}"
                )
            else:
                body = "매수매도에 오류가 발생하였습니다. 즉시 확인하길 바랍니다."
            
            # MIMEText 객체 생성
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            # SSL 연결 설정 및 이메일 전송
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, receiver_email, message.as_string())

            print("이메일이 성공적으로 전송되었습니다.")
        except Exception as e:
            print("오류입니다")
            print(e)

# 사용 예시
"""if __name__ == "__main__":
    sender_email = "cwnms171@gmail.com"
    app_password = "efuippuhknpgpxhy"
    receiver_email = "cwnms171@gmail.com"
    
    dt_info = DateTimeInfo()
    current_time = dt_info.get_datetime()
    
    email_sender = EmailSender(sender_email, app_password)
    email_sender.send_email(receiver_email, "BTC", current_time, 0.5, 0, 1000000, 0)"""




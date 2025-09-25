import schedule
import time
from datetime import datetime

# 1분 정각마다 실행할 함수
def print_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"현재 시간: {now}")

# 매 1분 정각마다 실행
schedule.every().minute.at(":00").do(print_time)

print("1분 정각마다 시간을 출력하는 프로그램 시작!")

while True:
    schedule.run_pending()
    time.sleep(1)  # CPU 점유율을 낮추기 위해 1초 대기


import schedule
import time
from datetime import datetime

class TimedTask:
    def __init__(self, hour, minute):
        """
        특정 시간(시:분)에 한 번만 실행되는 작업을 설정하는 클래스
        :param hour: 실행할 시간 (예: 14 → 오후 2시)
        :param minute: 실행할 분 (예: 30 → 30분)
        """
        self.hour = hour
        self.minute = minute
        self.scheduled = False  # 한 번만 실행을 위한 플래그
        self.schedule_task()

    def print_time(self):
        """현재 시간을 출력하는 함수"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"현재 시간: {now} - 설정된 시간 도달! 시간 체크 프로그램 종료.")
        self.scheduled = True  # 실행 플래그 변경

    def schedule_task(self):
        """설정된 특정 시간에 실행되는 스케줄링"""
        schedule.every().day.at(f"{self.hour:02d}:{self.minute:02d}").do(self.print_time)

    def run(self):
        """스케줄 실행 루프 (한 번 실행 후 종료)"""
        print(f"{self.hour:02d}:{self.minute:02d}에 실행하는 프로그램 시작!")
        while not self.scheduled:  # 실행될 때까지 대기
            schedule.run_pending()
            time.sleep(1)  # CPU 사용률 최적화를 위해 1초 대기
        print("매매 프로그램 시작.")

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

# 사용 예시
if __name__ == "__main__":
    dt_info = DateTimeInfo()
    print(dt_info.get_datetime())

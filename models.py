import calendar
from datetime import date, timedelta


class Shift:
    def __init__(self, working_days, days_off, start_time, end_time):
        self.working_days = working_days
        self.days_off = days_off
        self.start_time = start_time
        self.end_time = end_time


class Worker:
    def __init__(self, name, max_working_hours, work_day_length, shift: Shift):
        self.name = name
        self.max_working_hours = max_working_hours
        self.work_day_length = work_day_length
        self.shift = shift
        self.start_shift_date = None
        self.current_date = None

    def get_work_shifts(self):
        return self.max_working_hours // self.work_day_length

    def check_availability(self):
        return self.current_date - self.start_shift_date >= timedelta(days=30)

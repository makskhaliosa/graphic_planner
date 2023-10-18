from datetime import date
import calendar

from models import Shift, Worker

WORKERS_GRAPHIC = {}


def get_days_number_in_months(year: int):
    """Создает список с количеством дней в месяцах года."""
    days_number = ['']
    for i in range(1, 13):
        days_number.append(calendar.monthrange(year, i)[-1])
    return days_number


def get_worker_graphic(worker: Worker, start_work_date, year, month):
    """
    Считает даты рабочих дней и выходных для одного рабочего,
    возвращает кортеж со словарем графика и датой следующей смены.
    """
    days_in_months = get_days_number_in_months(year)
    month_days = days_in_months[month]
    days_off_period = worker.shift.days_off
    work_days_period = worker.shift.working_days
    work_period = worker.get_work_shifts()
    final_work_date = start_work_date + work_period * days_off_period - days_off_period
    count = 1
    day = start_work_date
    dates_of_work = {}
    for j in range(1, month_days + 1):
        if count > month_days:
            count -= month_days
        day_format = (year, month, count)
        dates_of_work[day_format] = 'off'
        count += 1

    def get_work_days():
        working_days = []
        work_periods = work_period // work_days_period
        work_day = start_work_date
        for period in range(work_periods):
            last_day = work_day + work_days_period
            for d in range(work_day, last_day):
                if d > month_days:
                    d -= month_days
                working_days.append(d)
            work_day = last_day + days_off_period
            if work_day > month_days:
                work_day -= month_days
        return working_days

    work_days = get_work_days()
    for i in range(start_work_date, final_work_date):
        if day > month_days:
            day -= month_days
            month = month + 1 if month < 12 else 1
        day_format = (year, month, day)
        dates_of_work[day_format] = (
            f'work {worker.shift.start_time} - {worker.shift.end_time}'
            if day in work_days
            else 'off'
        )
        day += 1
    return dates_of_work, (start_work_date + days_off_period)


def get_workers_graphic(workers: list[Worker], workers_in_one_shift, start_date, year, month):
    """Создает график для всех рабочих."""
    workers_count = 0
    for worker in workers:
        dates, next_shift = get_worker_graphic(worker, start_date, year, month)
        WORKERS_GRAPHIC[worker.name] = dates
        workers_count += 1
        if workers_count >= workers_in_one_shift:
            start_date = next_shift
            workers_count = 0


def get_text(info: dict):
    """Сохраняет график в файл."""
    text = []
    for k, v in info.items():
        tmp = [f'{k}: ']
        for d, g in v.items():
            year, month, day = d[0], d[1], d[2]
            weekday = date(year, month, day).strftime('%d %b %Y %A')
            txt = f'{weekday} ({g})'
            tmp.append(txt)
        text.append(' | '.join(tmp))
    output = ['\n\n'.join(text)]
    with open('graphic.txt', 'w', encoding='utf-8') as f:
        f.writelines('\n\n'.join(output))
        f.close()


WORKERS_COUNT = 1


def get_workers(workers_number, shift: Shift):
    """Создает тестовых рабочих."""
    global WORKERS_COUNT
    worker_list = []
    worker_name = 'test'
    for i in range(workers_number):
        new_worker = Worker(
            name=f'{worker_name}{WORKERS_COUNT}',
            max_working_hours=144,
            work_day_length=12,
            shift=shift
        )
        WORKERS_COUNT += 1
        worker_list.append(new_worker)
    return worker_list


def main():
    shift1 = Shift(2, 2, 8, 20)
    shift2 = Shift(2, 2, 10, 22)
    shift1_workers = get_workers(5, shift1)
    shift2_workers = get_workers(5, shift2)

    year = int(input('Введите год:'))
    month = int(input('Введите месяц в виде числа:'))
    start = int(input('С какого числа посчитать смены?'))

    get_workers_graphic(shift1_workers, 2, start, year, month)
    get_workers_graphic(shift2_workers, 1, start, year, month)
    get_text(WORKERS_GRAPHIC)


if __name__ == '__main__':
    main()

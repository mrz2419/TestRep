# Задача 1
# Написать программу, которая будет запускать процесс и с указанным
# интервалом времени собирать о нём следующую статистику:
# 
# Загрузка CPU (в процентах);
# 
# Потребление памяти: Working Set и Private Bytes (для Windows-систем)
# или Resident Set Size и Virtual Memory Size (для Linux-систем);
# 
# Количество открытых хендлов (для Windows-систем) или файловых
# дескрипторов (для Linux-систем).
# Сбор статистики должен осуществляться всё время работы запущенного
# процесса. Путь к файлу, который необходимо запустить, и интервал сбора
# статистики должны указываться пользователем. Собранную статистику
# необходимо сохранить на диске. Представление данных должно в дальнейшем
# позволять использовать эту статистику для автоматизированного построения
# графиков потребления ресурсов.

import datetime
import os
import sys
import subprocess
import csv
import psutil

_update_time = 10
_file_path = ''
_log_path = 'log.xml'


def main():
    init()
    exec_file()


def init():
    global _update_time, _file_path
    _update_time = input('Введте интервал (сек): ')
    _update_time = int(_update_time)
    if type(_update_time) is not int:
        print('Ошибка! Получен некорректный интервал!')
        sys.exit()
    _file_path = input('Введите путь к файлу: ')
    if not os.path.exists(_file_path):
        print('Ошибка! Файл не существует!')
        sys.exit()


def exec_file():
    global _update_time, _file_path
    proc = subprocess.Popen([_file_path])
    pid = proc.pid

    with open(_log_path, 'w', newline='') as logfile:
        writer = csv.writer(logfile)
        writer.writerow(['Time', 'CPU Usage', 'Working Set', 'Private Bytes', 'Open Handles'])
    init_time = datetime.datetime.now()
    while True:
        this_time = datetime.datetime.now()
        if (this_time - init_time).total_seconds() >= _update_time:
            python_process = psutil.Process(pid)
            with open(_log_path, 'a', newline='') as logfile:
                writer = csv.writer(logfile)
                writer.writerow([this_time, python_process.cpu_percent(), python_process.memory_percent(),
                                 python_process.memory_info()[11], python_process.num_handles()])
            init_time = this_time


if (__name__ == '__main__'):
    main()

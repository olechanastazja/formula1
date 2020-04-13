#!/usr/bin/env python
import schedule
from random import randrange
from Bolid import Bolid
from LogsReceiver import LogsReceiver


def send_info_from_bolid():
    temp, tire_pres, oil_pres = randrange(100), randrange(100), randrange(100)
    bolid = Bolid(temp, tire_pres, oil_pres)
    bolid.call()


def main():
    schedule.every(5).seconds.do(send_info_from_bolid)
    logs_receiver = LogsReceiver()
    logs_receiver.call()
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()

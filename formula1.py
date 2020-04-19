#!/usr/bin/env python
import schedule
from random import randrange
from Bolid import Bolid
from celery import Celery
from logs_receiver import LogsReceiver
from monitoring import Monitoring
from mechanic import Mechanic
from driver_client import DriverClient
from director import Director


app = Celery('formula1',
             backend='rpc://',
             broker='pyamqp://guest@localhost//')


def send_info_from_bolid():
    temp, tire_pres, oil_pres = randrange(100), randrange(100), randrange(100)
    bolid = Bolid(temp, tire_pres, oil_pres)
    bolid.call()


def ask_director_func():
    driver = DriverClient()
    driver.ask('Czy moge zjechac do pitstopu?')


def main():
    schedule.every(15).seconds.do(send_info_from_bolid)
    start_logging.delay()
    start_monitoring.delay()
    start_mechanic.delay()
    start_director.delay()
    schedule.every(17).seconds.do(ask_director_func)
    while True:
        schedule.run_pending()


@app.task
def start_logging():
    receive_logs = LogsReceiver()
    receive_logs.call()


@app.task
def start_monitoring():
    monitoring = Monitoring()
    monitoring.call()


@app.task
def start_mechanic():
    mechanic = Mechanic()
    mechanic.call()


@app.task
def start_director():
    director = Director()
    director.call()


if __name__ == '__main__':
    main()

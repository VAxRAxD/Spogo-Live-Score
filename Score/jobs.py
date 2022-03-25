from apscheduler.schedulers.background import BackgroundScheduler
from . fetch import *

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getMatchDetails,'interval', minutes=60)
    scheduler.add_job(getStats, 'interval', minutes=60)
    scheduler.start()
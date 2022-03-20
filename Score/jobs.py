from apscheduler.schedulers.background import BackgroundScheduler
from . fetch import *

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getMatchDetails,'interval', minutes=5)
    scheduler.add_job(getStats, 'interval', seconds=30)
    scheduler.start()
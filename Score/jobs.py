from apscheduler.schedulers.background import BackgroundScheduler
from . fetch import *

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getMatchDetails,'interval', minutes=5,max_instances=1)
    scheduler.add_job(getStats, 'interval', seconds=30,max_instances=1)
    scheduler.start()
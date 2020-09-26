from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', minute='*/20')
def scheduled_job():
    url = "https://data0manage.herokuapp.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

sched.start()

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def start_scheduler():
    from app.scheduler.clear_weakly_prediction_job import clear_daily_prediction_job
    scheduler.add_job(clear_daily_prediction_job, 'cron', hour=0, minute=0)
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()

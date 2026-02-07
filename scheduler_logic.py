import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta

# 1. Setup Persistence (SQLite)
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

def send_nudge(student_phone, topic_name, day_count):
    """Function to send the notification/quiz."""
    message = f"Day {day_count} Recall: Can you still explain {topic_name}?"
    print(f"Sending to {student_phone}: {message}")
    # Integration point: call your WhatsApp/Email function here

def schedule_1_4_7_nudges(student_phone, topic_name):
    """Schedules nudges for Day 1, 4, and 7 immediately upon Mastery."""
    intervals = [1, 4, 7]
    for day in intervals:
        run_time = datetime.now() + timedelta(days=day)
        scheduler.add_job(
            send_nudge, 
            'date', 
            run_time=run_time, 
            args=[student_phone, topic_name, day],
            id=f"{student_phone}_{topic_name}_day{day}"
        )
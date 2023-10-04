import logging
from apscheduler.events import EVENT_JOB_MISSED

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django_apscheduler.models import DjangoJob,DjangoJobExecution
from apscheduler import events

from offers.tasks import deactivate_offer
from rooms.tasks import end_maintenance,start_maintenance
from reservation.tasks import resolve_perma,resolve_temp

logger = logging.getLogger(__name__)

def test_task():
    print('Test Successful')

# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after our job has run.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.
    
    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def job_misfire_listener(event):
    if event.job_id == 'end_maintenance':
        print("Handeling 'end_maintenance' Exception...")
        end_maintenance()
        print("'end_maintenance' Exception Handeld")

    elif event.job_id == 'deactivate_offer':
        print("Handeling 'deactivate_offer' Exception...")
        deactivate_offer()
        print("'deactivate_offer' Exception Handeled")

    elif event.job_id == 'delete_old_job_executions':
        print("Handling 'delete_old_job_executions' Exception...")
        delete_old_job_executions()
        print("'delete_old_job_executions' Exception Handeled")

    elif event.job_id == 'start_maintenance':
        print("Handling 'start_maintenance' Exception...")
        start_maintenance()
        print("'start_maintenance' Exception Handeled")

    elif event.job_id == 'resolve_perma':
        print("Handling 'resolve_perma' Exception...")
        resolve_perma()
        print("'resolve_perma' Exception Handeled")

    elif event.job_id == 'resolve_temp':
        print("Handling 'resolve_temp' Exception...")
        resolve_temp()
        print("'resolve_temp' Exception Handeled")
        
    else:
        print("The Job ID Could Not Be Reached")


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self,*args, **kwargs):
        print('command running')
        scheduler = BlockingScheduler(timezone = settings.TIME_ZONE, misfire_grace_time=3600)
        scheduler.add_jobstore(DjangoJobStore(), "default") 

        if not DjangoJob.objects.filter(id ='end_maintenance' ).exists():
            scheduler.add_job(
                end_maintenance,
                trigger=CronTrigger(hour='0'),
                id='end_maintenance',
                max_instances=1,
                replace_existing=True,
                misfire_grace_time = 3600,
            )

            print("Added job 'end_maintenance'.") 

        if not DjangoJob.objects.filter(id = 'deactivate_offer').exists():
            scheduler.add_job(
                deactivate_offer,
                trigger=CronTrigger(hour='0'),
                id='deactivate_offer',
                max_instances=1,
                replace_existing=True,
                misfire_grace_time = 3600,
            )

            print("Added job 'delete_offer'.")

        if not DjangoJob.objects.filter(id ='start_maintenance' ).exists():
            scheduler.add_job(
                start_maintenance,
                trigger=CronTrigger(hour='0'),
                id='start_maintenance',
                max_instances=1,
                replace_existing=True,
                misfire_grace_time = 3600,
            )

            print("Added job 'end_maintenance'.") 

        if not DjangoJob.objects.filter(id ='resolve_perma' ).exists():
            scheduler.add_job(
                resolve_perma,
                trigger=CronTrigger(hour='12',minute='05'),
                id='resolve_perma',
                max_instances=1,
                replace_existing=True,
                misfire_grace_time = 3600,
            )

            print("Added job 'resolve_perma'.")

        if not DjangoJob.objects.filter(id ='resolve_temp' ).exists():
            scheduler.add_job(
                resolve_temp,
                trigger=CronTrigger(hour='21'),
                id='resolve_temp',
                max_instances=1,
                replace_existing=True,
                misfire_grace_time = 3600,
            )

            print("Added job 'resolve_temp'.") 

        if not DjangoJob.objects.filter(id ='delete_old_job_executions' ).exists():
            scheduler.add_job(
                delete_old_job_executions,
                trigger=CronTrigger(
                    day_of_week="mon", hour="00", minute="00"
                ),  # Midnight on Monday, before start of the next work week.
                id="delete_old_job_executions",
                max_instances=1,
                replace_existing=True,
            )

        print(
            "Added weekly job: 'delete_old_job_executions'."
        )

        scheduler.add_listener(job_misfire_listener,events.EVENT_JOB_MISSED)

        try:
            print("Starting scheduler...")
            scheduler.start()
            print("Scheduler Started")
        except KeyboardInterrupt:
            print("Stopping scheduler...")
            scheduler.shutdown()
            print("Scheduler shut down successfully!")
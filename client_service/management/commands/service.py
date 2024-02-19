from django_celery_beat.models import CrontabSchedule, PeriodicTask

schedule, _ = CrontabSchedule.objects.get_or_create(minute='1',
                                                    hour='*',
                                                    day_of_week='*',
                                                    day_of_month='*',
                                                    month_of_year='*')
periodic_task = PeriodicTask.objects.create(crontab=schedule, name='test-task', task='client_service.cron.sort_mailing')
periodic_task.enabled = True
periodic_task.save()
from django.apps import AppConfig

class StocksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stocks'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        from celery import current_app

        # Avoid duplicate registration
        if not PeriodicTask.objects.filter(name='Process Weekly Trades').exists():
            # Create interval schedule (1 week)
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.WEEKS
            )

            # Register the task
            PeriodicTask.objects.create(
                interval=schedule,
                name='Process Weekly Trades',
                task='stocks.celery.process_weekly_trades',
            )
            
class StocksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stocks"

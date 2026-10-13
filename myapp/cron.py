from django.utils import timezone
from django_cron import CronJobBase, Schedule
from myapp.models import Story


class CleanupExpiredStories(CronJobBase):
    RUN_EVERY = Schedule(run_every=3600)  # Run every hour

    def do(self):
        now = timezone.now()
        expired_stories = Story.objects.filter(expiry_time__lt=now)
        count = expired_stories.count()
        expired_stories.delete()
        print(f"Deleted {count} expired stories.")

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from wishwell.models import BucketItem
import datetime

class Command(BaseCommand):
    help = 'Sends email reminders for upcoming target dates within 3 days.'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        reminder_window = today + datetime.timedelta(days=3)

        upcoming_items = BucketItem.objects.filter(
            target_date__range=[today, reminder_window]
        ).exclude(status='Completed')

        count = 0
        for item in upcoming_items:
            if item.user.email:
                subject = f"🌊 Reminder: Your goal '{item.title}' is approaching!"
                message = f"Hello {item.user.username},\n\nYour bucket list item '{item.title}' has a target date scheduled for {item.target_date}.\n\nKeep moving in your Flow!\nWishWellMap Team"
                
                send_mail(
                    subject,
                    message,
                    'notifications@wishwellmap.com',
                    [item.user.email],
                    fail_silently=False,
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully processed and sent {count} email reminder(s)."))



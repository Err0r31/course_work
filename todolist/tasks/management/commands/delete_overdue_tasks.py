from django.core.management.base import BaseCommand
from tasks.models import Task
from django.utils import timezone

class Command(BaseCommand):
    help = 'Удалить все просроченные задачи, которые не завершены'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        overdue_tasks = Task.objects.filter(due_date__lt=now, is_completed=False)

        deleted_count = overdue_tasks.delete()

        self.stdout.write(self.style.SUCCESS(f'Удалено {deleted_count} просроченных задач'))
        
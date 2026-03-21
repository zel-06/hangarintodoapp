from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from tasktodomanager.models import Task, Category, Priority, SubTask, Note
import random

fake = Faker()

class Command(BaseCommand):
    help = "Generate initial fake data for Hangarin"

    def handle(self, *args, **kwargs):

        categories = Category.objects.all()
        priorities = Priority.objects.all()

        if not categories.exists() or not priorities.exists():
            self.stdout.write(self.style.ERROR(
                "Please create Category and Priority first in admin."
            ))
            return

        tasks = []

        # Create Tasks
        for i in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=random.choice(["Pending","In Progress","Completed"]),
                deadline=timezone.now(),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )

            tasks.append(task)

        # Create SubTasks
        for task in tasks:
            for i in range(random.randint(1,3)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=random.choice(["Pending","In Progress","Completed"])
                )

        for task in Task.objects.filter(id__lte=40):
            for i in range(random.randint(1, 3)):
                SubTask.objects.create(
            parent_task=task,
            title=fake.sentence(nb_words=4),
            status=random.choice(["Pending", "In Progress", "Completed"])
        )

        # Create Notes
        for task in tasks:
            for i in range(random.randint(1,2)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2)
                )

        self.stdout.write(self.style.SUCCESS("Fake Tasks, SubTasks, and Notes created successfully!"))

        # Create Notes only for tasks without notes
        for task in tasks:
            if not task.note_set.exists():   # ✅ check if task has notes
                for i in range(random.randint(1, 2)):
                    Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2)
            )

        self.stdout.write(self.style.SUCCESS("Fake Notes created for tasks without notes!"))

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
    
class Task(models.Model):
    class Status(models.TextChoices):
        Todo = "Todo", _("Todo")
        Inprogress = "Inprogress", _("Inprogress")
        Done = "Done", _("Done")

    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    due_date = models.DateField(blank=True)
    status = models.CharField(_("Task status"), choices=Status.choices, default=Status.Todo, max_length=50)
    members = models.ManyToManyField(User, related_name='tasks')


    def __str__(self):
        return self.title

from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=14)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Status"

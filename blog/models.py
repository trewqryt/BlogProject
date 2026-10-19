from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

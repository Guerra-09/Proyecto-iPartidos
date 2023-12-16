from django.db import models

# Create your models here.
class FrequentlyAskedQuestions(models.Model):
    title = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.title
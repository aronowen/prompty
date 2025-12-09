from django.db import models

class PromptSubmission(models.Model):
    name = models.CharField(max_length=100)
    prompt = models.TextField()
    score = models.IntegerField()

    def __str__(self):
        return f"{self.name} — {self.score}"
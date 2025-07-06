from django.db import models

class ScrapedItem(models.Model):
    name = models.CharField(max_length=512, unique=True)
    domains = models.JSONField(default=list)  # List of domain strings
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
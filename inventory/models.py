from django.db import models


class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=0)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
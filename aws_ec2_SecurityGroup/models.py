from django.db import models

class SecurityGroup(models.Model):
    group_id = models.CharField(max_length=100)
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name

from django.db import models

class AWSReport(models.Model):
    status = models.CharField(max_length=10)
    status_extended = models.TextField()
    check_metadata = models.JSONField()
    resource_details = models.TextField()
    resource_tags = models.JSONField()
    resource_id = models.CharField(max_length=100)
    resource_arn = models.CharField(max_length=255)
    region = models.CharField(max_length=50)
    
    def __str__(self):
        return f"AWS Report for {self.resource_id} in {self.region}"
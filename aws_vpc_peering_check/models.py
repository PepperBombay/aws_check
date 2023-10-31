# peering_monitor/models.py

from django.db import models

class VpcPeeringConnection(models.Model):
    connection_id = models.CharField(max_length=100)
    vpc_id = models.CharField(max_length=100)
    peer_vpc_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
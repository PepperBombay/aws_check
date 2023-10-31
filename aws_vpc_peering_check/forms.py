from django import forms

class VpcPeeringCheckForm(forms.Form):
    vpc_peering_id = forms.CharField(label='VPC Peering ID', max_length=100)
    aws_region = forms.CharField(label='AWS Region', max_length=50) 
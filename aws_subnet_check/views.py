# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import boto3

from .models import AWSReport

#vpc_id = 'vpc-084a7f72bd0a0b7e2'

def check_vpc_subnets(request, vpc_id,aws_region):
    # Initialize AWS SDK and VPC client
    aws_session = boto3.Session(region_name=aws_region)
    vpc_client = aws_session.client('ec2', region_name=aws_region)
    
    # Get VPC details
    vpc = vpc_client.describe_vpcs(VpcIds=[vpc_id])['Vpcs'][0]
    
    # 메인 기능 vpc subnet이 여러개의 가용영역을 지니고 있는지 체크
    availability_zones = set()
    for subnet in vpc_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['Subnets']:
        availability_zone = subnet['AvailabilityZone']
        availability_zones.add(availability_zone)
    
    # AWSReport instance 제작
    if len(availability_zones) > 1:
        report = AWSReport(
            status="PASS",
            status_extended="VPC has subnets in multiple availability zones",
            check_metadata={"description": "Check if VPC has subnets in multiple availability zones\\n"},
            resource_details=f"VPC ID: {vpc_id}\\n",
            resource_tags=vpc.get('Tags', []),
            resource_id=vpc_id,
            resource_arn=vpc['VpcId'],
            region='your_aws_region'
        )
    else:
        report = AWSReport(
            status="Security Vulnerability Found",
            status_extended="VPC has subnets in a single availability zone - Vulnerable to security. Place subnets in multiple available areas.",
            check_metadata={"description": "Check if VPC has subnets in multiple availability zones\\n"},
            resource_details=f"VPC ID: {vpc_id}\\n",
            resource_tags=vpc.get('Tags', []),
            resource_id=vpc_id,
            resource_arn=vpc['VpcId'],
            region='your_aws_region'
        )
    
    # database에 결과 저장
    report.save()

    # json 파일 만들기
    response_data = {
        'message': 'Check complete',
        'result': report.status,
        'status_extended': report.status_extended,
        'check_metadata': report.check_metadata,
        'resource_details': report.resource_details,
        'resource_tags': report.resource_tags,
        'resource_id': report.resource_id,
        'resource_arn': report.resource_arn,
        'region': report.region,
    }

    return JsonResponse(
        response_data
        #{'message': 'Check complete', 'result': report.status,}
    )

    """
    return JsonResponse({
        'message': 'Check complete', 'result': report.status,
        'status_extended' : report.status_extended,
        'check_metadata' : report.check_metadata,
        'resource_details' : report.resource_details,
        'resource_tags' : report.resource_tags,
        'resource_id' : report.resource_id,
        'resource_arn' : report.resource_arn,
        'region' : report.region,
    })"""
    #http://localhost:8000/aws-subnet-check/vpc-084a7f72bd0a0b7e2/ap-northeast-2/

from django.shortcuts import render
import boto3
from .models import Subnet

def get_subnets(request):
    ec2 = boto3.client('ec2')
    subnets = ec2.describe_subnets()
    
    for subnet in subnets['Subnets']:
        subnet_id = subnet['SubnetId']
        vpc_id = subnet['VpcId']
        cidr_block = subnet['CidrBlock']
        
        # 서브넷의 라우팅 테이블을 가져옴
        routing_table = ec2.describe_route_tables(Filters=[{'Name': 'association.subnet-id', 'Values': [subnet_id]}])
        
        # 라우팅 테이블에 인터넷 게이트웨이 또는 NAT 게이트웨이 연결 여부 확인 - 왜냐하면 서브넷의 라우트 테이블을 기반으로 판단해야 하기 떄문
        # 공용 서브넷은 인터넷 gateway와 연결된 라우팅 테이블을, 프라이빗은 NAT gatewaay나 NAT 인스턴스와 연결된 라우팅 테이블을 가짐 - 이를 통해 판단
        is_public = False
        for rt in routing_table['RouteTables']:
            for route in rt['Routes']:
                if 'GatewayId' in route and (route['GatewayId'].startswith('igw-') or route['GatewayId'].startswith('nat-')):
                    is_public = True
                    break
        
        Subnet.objects.update_or_create(
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            cidr_block=cidr_block,
            is_public=is_public,
        )
    
    subnets = Subnet.objects.all()
    
    return render(request, 'subnets.html', {'subnets': subnets})
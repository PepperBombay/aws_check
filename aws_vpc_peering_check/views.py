import boto3
from django.shortcuts import render
from django.http import JsonResponse
from forms import VpcPeeringCheckForm


def check_vpc_peering_permissions(request):
    if request.method == 'POST':
        form = VpcPeeringCheckForm(request.POST)
        if form.is_valid():
            vpc_peering_id = form.cleaned_data['vpc_peering_id']
            aws_region = form.cleaned_data['aws_region']
            
            # AWS SDK 및 EC2 클라이언트 초기화
            aws_session = boto3.Session(region_name=aws_region)
            ec2_client = aws_session.client('ec2', region_name=aws_region)
            
            # VPC 피어링 연결에 대한 정보 가져오기
            peering_connection = ec2_client.describe_vpc_peering_connections(
                VpcPeeringConnectionIds=[vpc_peering_id]
            )['VpcPeeringConnections'][0]
            
            # 여기서 라우팅 테이블에 대한 권한을 확인
            # 권한 검사와 로직 여기에 추가 예정
        
            is_active = peering_connection['Status']['Code'] == 'active' #예시: 피어링 연결이 활성화되어 있는지 확인
            
            return JsonResponse({'message': '검사 완료', 'is_active': is_active})
    else:
        form = VpcPeeringCheckForm()
    
    return render(request, 'check_vpc_peering_permissions.html', {'form': form})

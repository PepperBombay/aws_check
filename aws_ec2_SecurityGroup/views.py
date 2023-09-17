import boto3
from django.http import JsonResponse

def get_security_group_info(request, instance_id):
    try:
        ec2_client = boto3.client('ec2', region_name='ap-northeast-2')

        # 인스턴스 ID를 사용하여 보안 그룹 ID 가져오기
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        security_group_ids = []

        if 'Reservations' in response:
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    for sg in instance['SecurityGroups']:
                        security_group_ids.append(sg['GroupId'])

        # 보안 그룹 정보 가져오기
        security_group = ec2_client.describe_security_groups(GroupIds=security_group_ids)['SecurityGroups'][0]

        # 정보 추출
        group_id = security_group['GroupId']
        group_name = security_group['GroupName']
        inbound_rules = security_group.get('IpPermissions', [])
        outbound_rules = security_group.get('IpPermissionsEgress', [])

        # 추출한 정보를 JSON으로 반환
        data = {
            'group_id': group_id,
            'group_name': group_name,
            'inbound_rules': inbound_rules,
            'outbound_rules': outbound_rules,
        }

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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

        if not security_group_ids:
            return JsonResponse({'warning': '보안 그룹이 존재하지 않습니다. 보안 그룹을 생성하세요.'})

        # 모든 보안 그룹 정보 가져오기
        security_groups = ec2_client.describe_security_groups(GroupIds=security_group_ids)['SecurityGroups']

        security_group_data = []
        for security_group in security_groups:
            group_id = security_group['GroupId']
            group_name = security_group['GroupName']
            inbound_rules = security_group.get('IpPermissions', [])
            outbound_rules = security_group.get('IpPermissionsEgress', [])

            group_data = {
                'group_id': group_id,
                'group_name': group_name,
                'inbound_rules': inbound_rules,
                'outbound_rules': outbound_rules,
            }
            security_group_data.append(group_data)
            # 경고 메시지 추가
            if any(rule.get('IpRanges', [{'CidrIp': '0.0.0.0/0'}])[0]['CidrIp'] == '0.0.0.0/0' for rule in
                   inbound_rules):
                warning_message = '경고: 인바운드 규칙이 모든 IP 허용으로 설정되어 있습니다. 최소한의 IP만 허용하십시오.'
                security_group_data.append({'warning': warning_message})



        return JsonResponse({'security_groups': security_group_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

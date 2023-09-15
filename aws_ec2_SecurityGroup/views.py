import boto3
from django.http import JsonResponse  # JSON 응답 반환

def get_security_group_info(request, security_group_id):
    try:
        ec2_client = boto3.client('ec2', region_name='ap-northeast-2')

        # 보안 그룹 정보 가져오기
        response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
        security_group = response['SecurityGroups'][0]

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
        return JsonResponse({'error': str(e)}, status=500)  # 서버 오류 응답


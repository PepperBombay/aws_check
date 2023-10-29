from django.http import JsonResponse
import boto3
from datetime import datetime, timedelta

def check_instance_creation_date(request, instance_id):
    # AWS 자격 증명 및 EC2 클라이언트 생성
    ec2 = boto3.client('ec2', region_name='ap-northeast-2')
    try:
        # EC2 인스턴스 정보 조회
        response = ec2.describe_instances(InstanceIds=[instance_id])
        if not response['Reservations']:
            return JsonResponse({"message": "Instance not found"})

        instance = response['Reservations'][0]['Instances'][0]
        launch_time = instance['LaunchTime']

        # 오늘 날짜를 가져옴
        today = datetime.now()

        # 경과일 계산
        elapsed_days = (today - launch_time).days

        if elapsed_days > 180:
            message = "경고: 인스턴스가 생성된 지 180일 이상 경과했습니다. 보안 설정을 다시 검토하십시오. "
        else:
            message = "인스턴스는 180일 이내에 생성되었습니다."

        result = {
            "InstanceId": instance_id,
            "LaunchTime": launch_time.strftime('%Y-%m-%d %H:%M:%S'),
            "ElapsedDays": elapsed_days,
            "Message": message
        }

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({"error": str(e)})

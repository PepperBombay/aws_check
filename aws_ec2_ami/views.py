import boto3
import json
from django.http import JsonResponse

def get_instance_ami_id(instance_id):
    # Boto3 EC2 클라이언트 생성

    ec2 = boto3.client('ec2', region_name='ap-northeast-2')

    try:
        # 인스턴스 IDgit를 사용하여 EC2 인스턴스 정보 조회
        response = ec2.describe_instances(InstanceIds=[instance_id])

        if len(response['Reservations']) > 0:
            instance = response['Reservations'][0]['Instances'][0]
            ami_id = instance['ImageId']
            return ami_id
        else:
            return None  # 인스턴스가 없을 경우 None 반환
    except Exception as e:
        return None  # 오류 발생 시 None 반환

def check_ami_public(request, instance_id):
    ami_id = get_instance_ami_id(instance_id)

    if ami_id is None:
        result = {"message": "Instance not found or error occurred."}
    else:
        # Boto3 EC2 클라이언트 생성
        ec2 = boto3.client('ec2', region_name='ap-northeast-2')

        try:
            response = ec2.describe_images(ImageIds=[ami_id])

            if len(response['Images']) > 0:
                image = response['Images'][0]
                is_public = image['Public']

                if is_public:
                    result = {
                        "ami_id": ami_id,
                        "message": "경고: AMI가 공개적으로 사용 가능한 상태입니다."
                    }
                else:
                    result = {
                        "ami_id": ami_id,
                        "message": "안전: AMI가 공개적으로 사용 가능하지 않은 상태입니다."
                    }
            else:
                result = {"message": f"AMI {ami_id} not found."}
        except Exception as e:
            result = {"message": f"Error: {str(e)}"}

    return JsonResponse(result)

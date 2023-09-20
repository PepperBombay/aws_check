# iam_policy/views.py
from django.shortcuts import render
from django.http import HttpResponse
import boto3
import json

def Root_MFA_Check(request):
    # 정책 문서 로드
    with open('iam_policy/Root_MFA_Check/Root_MFA_Check.json', 'r') as file:
        policy_document = json.load(file)

    # Boto3 세션 및 IAM 클라이언트를 설정
    session = boto3.Session(profile_name='user1')
    iam = session.client('iam')

    PolicyName = 'Root_MFA_Check'

    # 동일한 이름의 정책이 존재하는지 확인
    existing_policies = iam.list_policies(Scope='Local')
    policy_exists = any(policy['PolicyName'] == PolicyName for policy in existing_policies['Policies'])

    if not existing_policies:
        # IAM 정책 생성(response에 생성에 대한 응답을 저장)
        response = iam.create_policy(PolicyName, PolicyDocument=json.dumps(policy_document))  # JSON 형식으로 변환

    # 유저 정보를 가져옵니다 (root인지 확인하기 위함)
    current_user = iam.get_user()
    user_name = current_user['User']['UserName']

    # 현재 계정이 Root인지 확인
    if user_name == 'root':
        root_mfa_enabled = current_user['User']['MFADevices']

        # 루트 계정이 MFA를 사용하지 않는 경우 알림 출력
        if not root_mfa_enabled:
            message += "경고: 루트 계정이 MFA를 사용하지 않습니다. 접근을 위해 MFA를 활성화하세요.<br>"
        else:
            message += "루트 계정은 MFA를 사용하고 있습니다.<br>"
    else:
        message += "현재 사용자는 루트 계정이 아닙니다.<br>"

    return HttpResponse(message)
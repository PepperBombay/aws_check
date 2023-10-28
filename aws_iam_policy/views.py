# iam_policy/views.py
from django.shortcuts import render
from django.http import HttpResponse
import boto3
import json
import re

def Create_Policy(iam, PolicyName):  #IAM 세션과 ,정책명을 받아서 정책을 생성하는 함수
    policy_path = 'aws_iam_policy/' + PolicyName + '/' + PolicyName + '.json'
    with open(policy_path, 'r') as file:
        policy_document = json.load(file)
    existing_policies = iam.list_policies(Scope='Local')
    policy_exists = any(policy['PolicyName'] == PolicyName for policy in existing_policies['Policies'])
    if not policy_exists:
        # IAM 정책 생성(response에 생성에 대한 응답을 저장)
        response = iam.create_policy(PolicyName=PolicyName, PolicyDocument=json.dumps(policy_document))
        message = f"정책 '{PolicyName}'이 생성되었습니다.<br>"
    else:
        message = f"정책 '{PolicyName}'이 이미 존재합니다.<br>"
    return message

def Root_MFA_Check(request):
    # Boto3 세션 및 IAM 클라이언트를 설정
    session = boto3.Session(profile_name='user1')
    iam = session.client('iam')
    
    PolicyName = 'Root_MFA_Check'
    message = Create_Policy(iam, PolicyName)

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

def Password_Policy(request):    #패스워드 변경시 IAM정책 생성
    session = boto3.Session(profile_name='user1')
    iam = session.client('iam')
    message = ""
    PolicyName = 'Password_Policy'
    message += Create_Policy(iam, PolicyName)
    
    '''     패스워드 검사 함수 확인용
    passwd = "asdfASDFa#"
    mess, able = CheckPassword(passwd)
    message += mess
    '''

    return HttpResponse(message)

def CheckPassword(passwd):
    session = boto3.Session(profile_name='user1')
    iam = session.client('iam')

    if len(passwd) < 10 or not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$])[\S]{10,}$", passwd):
        message = f"비밀번호는 10자 이상이어야 하며, (숫자, 소문자, 대문자, 특수문자)를 모두 포함해야 합니다.<br>"
        passwdable = False
    else:
        message = f"비밀번호를 사용할 수 있습니다.<br>"
        passwdable = True
            
    return message, passwdable

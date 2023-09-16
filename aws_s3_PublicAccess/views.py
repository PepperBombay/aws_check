# myapp/views.py

from django.shortcuts import render
from .s3_security_check import perform_s3_bucket_security_check

def s3_security_check_view(request):
    result = perform_s3_bucket_security_check()
    return render(request, 'aws_s3_PublicAccess/s3_security_check.html', {'result': result})

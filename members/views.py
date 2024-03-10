import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Member
from .runner import validate
from .utils import create_register_key
from .crypto import encrypt, decrypt

@csrf_exempt
def signup(request: HttpRequest) -> HttpResponse:
    body = json.loads(request.body)
    
    student_id = body['student_id']
    password = body['password']
    
    query = Member.objects.filter(student_id=student_id)
    
    if query.exists():
        member = query[0]
        
        if encrypt(password) != member.password:
            return JsonResponse({'code': 2, 'error': '잘못된 id 또는 비밀번호입니다.'}, status=400)
        
    else:
        if not validate(student_id, password):
            return JsonResponse({'code': 1, 'error': '잘못된 id 또는 비밀번호입니다.'}, status=400)
        
        register_key = create_register_key()
        member = Member(student_id=student_id, password=password, register_key=register_key)
        member.save()
        
    

    return JsonResponse({'register_key': register_key})
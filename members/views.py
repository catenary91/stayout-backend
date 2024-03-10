import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Member
from .runner import validate
from .utils import create_register_key
from .crypto import encrypt, decrypt
from .kakao_response import Blocks, Menu, TextResponse, TextMenuResponse

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


def register(request: HttpRequest) -> HttpRequest:
    body = json.loads(request.body)
    
    user_key = body['userRequest']['user']['id']
    register_key = body['action']['params']['register_key']
    
    query = Member.objects.filter(register_key=register_key)
    if not query.exists():
        return TextMenuResponse('유효하지 않은 등록 키입니다.', [Menu('다시 입력하기', Blocks.REGISTER), Menu('가입하러 가기', Blocks.SIGNUP)])
    
    member = query[0]
    member.user_key = user_key
    
    return TextMenuResponse(f'카카오 계정이 등록되었습니다.\nID: {member.student_id}', [Menu('외박신청하기', Blocks.APPLY)])
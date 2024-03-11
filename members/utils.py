import random, json
from typing import Callable
from django.http import HttpRequest, HttpResponse, JsonResponse

from .models import Member
from .kakao_response import Blocks, Menu, TextMenuResponse

def create_register_key() -> str:
    while True:
        key = hex(random.randint(0x100000, 0xFFFFFF))[2:]
        
        if Member.objects.filter(register_key=key).exists():
            continue
        
        break
    
    return key

def need_registeration(view: Callable[[HttpRequest, Member], JsonResponse]) -> Callable[[HttpRequest], JsonResponse]:

    def wrapper(request: HttpRequest):
        body = json.loads()
        user_key = body['userRequest']['user']['id']
        
        query = Member.objects.filter(user_key=user_key)
        if not query.exists():
            return TextMenuResponse('등록되지 않은 계정입니다.', [Menu('가입하러 가기', Blocks.SIGNUP), Menu('인증코드 입력하기', Blocks.REGISTER)])

        return view(request, query[0])

    return wrapper
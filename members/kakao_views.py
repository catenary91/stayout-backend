import json
from django.http import HttpRequest, HttpResponse

from .models import Member
from .utils import need_registeration
from .crypto import decrypt
from .kakao_response import Blocks, Menu, TextMenuResponse
from .runner import get_history, apply

def register_view(request: HttpRequest) -> HttpRequest:
    body = json.loads(request.body)
    
    user_key = body['userRequest']['user']['id']
    register_key = body['action']['params']['register_key']
    
    query = Member.objects.filter(register_key=register_key)
    if not query.exists():
        return TextMenuResponse('유효하지 않은 등록 키입니다.', Menu('다시 입력하기', Blocks.REGISTER), Menu('가입하러 가기', Blocks.SIGNUP))
    
    member = query[0]
    member.user_key = user_key
    
    return TextMenuResponse(f'카카오 계정이 등록되었습니다.\nID: {member.student_id}', Menu('외박 신청하기', Blocks.APPLY), Menu('외박 신청 조회', Blocks.GET_HISTORY))

@need_registeration
def get_history_view(request: HttpRequest, member: Member) -> HttpResponse:

    history = get_history(member.student_id, decrypt(member.password))
    history_str = map(lambda h: f'신청일:{h[0]}\n{h[1]} / {h[2]}', history)

    return TextMenuResponse(history_str, Menu('외박 신청하기', Blocks.APPLY), Menu('외박 신청 조회', Blocks.GET_HISTORY))

@need_registeration
def apply_view(request: HttpRequest, member: Member) -> HttpResponse:
    body = json.loads(request.body)

    start_date = body['action']['params']['start_date']
    end_date = body['action']['params']['end_date']

    apply(member.student_id, decrypt(member.password), start_date, end_date)

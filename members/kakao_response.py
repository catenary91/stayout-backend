from typing import Any, List
from django.http import JsonResponse

class Blocks:
    REGISTER = '65ec4a6e600b300bd7176d88'
    APPLY = '65ec46377b3c255fa3724639'
    SIGNUP = '65ed71f90a73415ce06b059d'
    
def Menu(label: str, block_id: str, message_text: str = ''):
    if message_text == '':
        message_text = label
        
    return {
        "label": label,
        "action": "block",
        "messageText": message_text,
        "blockId": block_id,
    }

def TextResponse(text: str) -> JsonResponse:
    return JsonResponse({
        "veresion": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    })
    
def TextMenuResponse(text: str, *menu: List[Any]) -> JsonResponse:
    return JsonResponse({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ],
            "quickReplies": list(menu)
        }
    })
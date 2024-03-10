import random

from .models import Member

def create_register_key() -> str:
    while True:
        key = hex(random.randint(0x100000, 0xFFFFFF))[2:]
        
        if Member.objects.filter(register_key=key).exists():
            continue
        
        break
    
    return key
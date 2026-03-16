from pydantic import BaseModel

class MemberRequest(BaseModel):
    member_id: str
    name: str
    email: str
    phone: str
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.models import MemberRequest
from src.database import (
    get_all_members, get_member, save_member,
    update_member, delete_member, member_exists
)

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/members")
async def list_members():
    return await get_all_members()

@app.get("/members/{member_id}")
async def get_single_member(member_id: str):
    member = await get_member(member_id)
    if not member:
        return JSONResponse(
            status_code=404,
            content={"detail": "Üye bulunamadı"}
        )
    return member

@app.post("/members", status_code=201)
async def add_member(request: MemberRequest):
    if await member_exists(request.member_id):
        return JSONResponse(
            status_code=400,
            content={"detail": "Bu ID ile üye zaten mevcut"}
        )
    await save_member(
        member_id=request.member_id,
        name=request.name,
        email=request.email,
        phone=request.phone
    )
    return {"message": "Üye başarıyla eklendi"}

@app.put("/members/{member_id}")
async def update_single_member(member_id: str, request: MemberRequest):
    if not await member_exists(member_id):
        return JSONResponse(
            status_code=404,
            content={"detail": "Üye bulunamadı"}
        )
    await update_member(
        member_id=member_id,
        name=request.name,
        email=request.email,
        phone=request.phone
    )
    return {"message": "Üye başarıyla güncellendi"}

@app.delete("/members/{member_id}")
async def delete_single_member(member_id: str):
    if not await member_exists(member_id):
        return JSONResponse(
            status_code=404,
            content={"detail": "Üye bulunamadı"}
        )
    await delete_member(member_id)
    return {"message": "Üye başarıyla silindi"}
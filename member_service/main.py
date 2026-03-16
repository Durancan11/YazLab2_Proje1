from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.models import MemberRequest
from src.service import (
    fetch_all_members, fetch_member,
    add_member, modify_member, remove_member
)

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/members")
async def list_members():
    return await fetch_all_members()

@app.get("/members/{member_id}")
async def get_single_member(member_id: str):
    member = await fetch_member(member_id)
    if not member:
        return JSONResponse(
            status_code=404,
            content={"detail": "Üye bulunamadı"}
        )
    return member

@app.post("/members", status_code=201)
async def add_single_member(request: MemberRequest):
    success, message = await add_member(
        member_id=request.member_id,
        name=request.name,
        email=request.email,
        phone=request.phone
    )
    if not success:
        return JSONResponse(
            status_code=400,
            content={"detail": message}
        )
    return {"message": message}

@app.put("/members/{member_id}")
async def update_single_member(member_id: str, request: MemberRequest):
    success, message = await modify_member(
        member_id=member_id,
        name=request.name,
        email=request.email,
        phone=request.phone
    )
    if not success:
        return JSONResponse(
            status_code=404,
            content={"detail": message}
        )
    return {"message": message}

@app.delete("/members/{member_id}")
async def delete_single_member(member_id: str):
    success, message = await remove_member(member_id)
    if not success:
        return JSONResponse(
            status_code=404,
            content={"detail": message}
        )
    return {"message": message}
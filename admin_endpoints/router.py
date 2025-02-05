from fastapi import APIRouter, HTTPException, status, Request, Response
from models.dao import UserDAO
from models.auth import check_token, get_password_hash
from models.schemas import CreateUserSchema, UserUpdateSchema, AllUsersResponseSchema
from typing import List


router = APIRouter(prefix='/admin', tags=['Admin'])


async def check_admin(token):
    user_id = check_token(token)
    is_admin = await UserDAO.check_admin(user_id)
    if not is_admin:    
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You are not admin')
    return is_admin


@router.get('/users')
async def get_users(token: str):
    await check_admin(token)
    q = await UserDAO.find_all_without_filter()
    return q

@router.post('/users/create')
async def create_user(token: str, item: CreateUserSchema):
    await check_admin(token)
    hashed_password = get_password_hash(item.password)
    await UserDAO.add(email=item.email, full_name=item.full_name, hashed_password=hashed_password, is_admin=item.is_admin)
    return {'status': 'success'}

@router.post('/users/update_user')
async def update_user(token: str, pk: int, item: UserUpdateSchema):
    await check_admin(token)
    await UserDAO.update_by_id(pk, item)
    return {'status': 'success'}

@router.post('/users/delete')
async def delete_user(token: str, pk: int):
    await check_admin(token)
    user = await UserDAO.delete_by_id(pk)
    return {'status': 'success'}
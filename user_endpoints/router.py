from fastapi import APIRouter, HTTPException, status, Request, Response
from models.dao import UserDAO, AccountDAO, TransactionDAO
from models.auth import check_token
from models.schemas import AccountsResponse, TransactionSchema
from typing import List


router = APIRouter(prefix='/user', tags=['User'])


async def check_user(data_id):
    user = await UserDAO.find_one_or_none_by_id(data_id)
    if not user:
        raise HTTPException(status=status.HTTP_400_BAD_REQUEST, detail='User doesnt exist')
    return user


@router.get('/me')
async def get_me(token: str):
    user_id = check_token(token)
    user = await check_user(user_id)
    return {'id': user.id, 'email': user.email, 'full_name': user.full_name}


@router.get('/accounts', response_model=List[AccountsResponse])
async def get_accounts(token: str):
    user_id = check_token(token)
    await check_user(user_id)
    accs = await AccountDAO.get_accounts(user_id)
    return accs


@router.get('/trs', response_model=List[TransactionSchema])
async def get_trs(token: str):
    user_id = check_token(token)
    await check_user(user_id)
    trs = await TransactionDAO.find_all()
    return trs or [{'unq_id': '-1', 'amount': -1}]



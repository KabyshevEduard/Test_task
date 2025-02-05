from fastapi import APIRouter, HTTPException, status, Request, Response
from models.dao import UserDAO
from models.auth import check_token, get_signature, check_signature, SECRET_KEY
from models.schemas import WebHookSchema
from typing import List


router = APIRouter(prefix='/transact', tags=['Transaction'])


@router.post('/send')
async def web_tr(token: str, item: WebHookSchema):
    '''
        transaction_id: str = qqoqoqoo
        account_id: int = 2
        user_id: int = 2
        amount: float = 140.0
        signature: str = $5$rounds=535000$XUBpx45eyxOhLnMD$Yv.mpd8c4wK5iuIqlcaDYhl2R4SwifA5pkWKnZuUu01
    '''
    sgn = str(item.account_id) + str(item.amount) + str(item.transaction_id) + str(item.user_id) + str(SECRET_KEY)
    if not check_signature(sgn, item.signature):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Bad signature')
    
    user = await UserDAO.update_account_transaction(item.user_id, account_id=item.account_id, amount=item.amount, unq_id=item.transaction_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Something wrong')
    
    return {'status': 'success'}
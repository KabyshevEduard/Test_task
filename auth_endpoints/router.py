from fastapi import APIRouter, HTTPException, status
from models.auth import verify_password, get_password_hash, create_access_token
from models.dao import UserDAO
from models.schemas import UserRegisterSchema, UserLoginSchema


router = APIRouter(prefix='/auth_user', tags=['Authenticate'])


async def authenticate_user(email, password):
    user = await UserDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user


@router.post('/reg')
async def register(item: UserRegisterSchema):
    user = await UserDAO.find_one_or_none(email=item.email)
    if user:
        return {'status': 'User already exist'}

    hashed_password = get_password_hash(item.password)
    try:
        await UserDAO.add(email=item.email, full_name=item.full_name, hashed_password=hashed_password, is_admin=False)
        return {'status': 'success'}
    except Exception as e:
        return {'status': str(e)}


@router.post('/log')
async def login(item: UserLoginSchema):
    user = await authenticate_user(email=item.email, password=item.password)
    if user == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email or password are incorrect')
    
    return {'status': 'logged_in', 'token': create_access_token({'sub': str(user.id)})}

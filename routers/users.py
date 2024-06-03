from fastapi import APIRouter, HTTPException, Depends
import Validators
from typing import Annotated
from sqlalchemy.orm import Session

import utils.CommonFunctions
from connection.database import SessionLocal, engine
from models import user_model
from routers import investors


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_model.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]
user_router = APIRouter()

# Register the blueprint with a custom URL prefix
user_router.include_router(
    investors.investors_router,
    prefix="/investors"
)


@user_router.get('/')
async def user_details(wallet_address: str, db: db_dependency):

    if not wallet_address:
        raise HTTPException(status_code=500, detail="wallet_address missing")

    try:
        result = db.query(user_model.Users).filter(user_model.Users.wallet_address == wallet_address).first()
        auth_id: str = getattr(result, 'auth_id', None)

        trade_history = db.query(user_model.TradeHistory).filter(user_model.TradeHistory.user_id == auth_id).all()

        if not result:
            return {'message': 'User not found'}

        return {'message': result, 'trade_history': trade_history}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the user! {e}")


@user_router.get('/all')
async def users_details(db: db_dependency):

    try:
        result = db.query(user_model.Users).all()
        return {'message': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the users! {e}")


@user_router.patch('/login')
async def user_login(payload: Validators.login_user_validator.LoginUser, db: db_dependency):
    if not payload:
        raise HTTPException(status_code=500, detail="auth_id missing")
    try:
        user_db = db.query(user_model.Users).filter(user_model.Users.auth_id == payload.auth_id).first()

        if user_db.blocked:
            return {'message': 'User Blocked'}

        user_db.last_online = utils.CommonFunctions.today_seconds()
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return {'message': 'Success'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to login the user! {e}")


@user_router.patch('/change_name')
async def change_name_user(payload: Validators.change_name_user_validator.ChangeNameUser, db: db_dependency):
    if not payload:
        raise HTTPException(status_code=500, detail="auth_id missing")
    try:
        user_db = db.query(user_model.Users).filter(user_model.Users.auth_id == payload.auth_id).first()
        user_db.name = payload.name
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return {'message': 'Success'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to change the name of the user! {e}")


@user_router.patch('/block')
async def toggle_user_status(payload: Validators.block_user_validator.BlockUser, db: db_dependency):
    if not payload:
        raise HTTPException(status_code=500, detail="auth_id missing")
    try:
        user_db = db.query(user_model.Users).filter(user_model.Users.auth_id == payload.auth_id).first()

        user_db.blocked = payload.block
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return {'message': user_db}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to login the user! {e}")


@user_router.post('/create')
async def create_user(details: Validators.create_user_validator.UserBase, db: db_dependency):
    try:
        # Get today seconds
        today_epoch_time = utils.CommonFunctions.today_seconds()

        # Create the user table
        db_users = user_model.Users(
            auth_id=details.auth_id,
            wallet_address=details.wallet_address,
            registration_date_time=today_epoch_time,
            last_online=today_epoch_time,
            total_investments=details.total_investments,
            user_type=details.user_type,
            dividend_wallet=details.dividend_wallet
        )
        db.add(db_users)
        db.commit()
        db.refresh(db_users)

        return {'message': 'Success'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to create the user! {e}")

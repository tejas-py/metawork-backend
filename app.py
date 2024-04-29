from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session

import utils.CommonFunctions
from connection.database import SessionLocal, engine
from models import user_model
import Validators

# Configure app
app = FastAPI()
user_model.Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def home_page():
    return RedirectResponse("https://metawork-wallet.vercel.app", status_code=302)


@app.post('/user/create/')
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
            user_type=details.user_type
        )
        db.add(db_users)
        db.commit()
        db.refresh(db_users)

        # create holdings table
        if details.holding:
            for asset_balance in details.holding:
                db_holding = user_model.Holdings(
                    token=asset_balance.token,
                    balance=asset_balance.balance,
                    user_id=db_users.auth_id
                )
                db.add(db_holding)
        db.commit()
        db.refresh(db_users)

        # Create the yield table
        if details.total_yield:
            for dividend in details.total_yield:
                db_dividend = user_model.TotalYield(
                    asset_name=dividend.asset_name,
                    time=dividend.time,
                    units=dividend.units,
                    user_id=db_users.auth_id
                )
                db.add(db_dividend)
        db.commit()
        db.refresh(db_users)

        # create the trade history table
        if details.trade_history:
            for trade in details.trade_history:
                db_trade = user_model.TradeHistory(
                    asset_name=trade.asset_name,
                    amount=trade.amount,
                    price=trade.price,
                    time=trade.time,
                    trade_type=trade.trade_type,
                    user_id=db_users.auth_id
                )
                db.add(db_trade)
        db.commit()
        db.refresh(db_users)
        return {'message': 'Success'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to create the user! {e}")


@app.get('/user/')
async def user_details(wallet_address: str, db: db_dependency):

    if not wallet_address:
        raise HTTPException(status_code=500, detail="wallet_address missing")

    try:
        result = db.query(user_model.Users).filter(user_model.Users.wallet_address == wallet_address).first()
        auth_id: str = getattr(result, 'auth_id', None)

        trade_history = db.query(user_model.TradeHistory).filter(user_model.TradeHistory.user_id == auth_id).all()
        total_yield = db.query(user_model.TotalYield).filter(user_model.TotalYield.user_id == auth_id).all()

        if not result:
            return {'message': 'User not found'}

        return {'message': result, 'trade_history': trade_history, 'total_yield': total_yield}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the user! {e}")


@app.get('/user/investors/investments')
async def investor_investments(db: db_dependency):

    try:
        result = db.query(user_model.Users).all()

        total_investment = 0
        for investor_detail in result:
            investment = investor_detail.total_investments
            total_investment += investment

        return {'message': total_investment}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the investments! {e}")


@app.get('/user/all')
async def users_details(db: db_dependency):

    try:
        result = db.query(user_model.Users).all()
        return {'message': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the users! {e}")


@app.get('/user/investors/trade_history')
async def investors_trade_history(db: db_dependency):

    try:
        result = db.query(user_model.TradeHistory).all()
        return {'message': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the investors trade history! {e}")


@app.get('/user/investors/yield')
async def investors_yield(db: db_dependency):

    try:
        result = db.query(user_model.TotalYield).all()
        return {'message': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the investors total yield! {e}")


@app.post('/user/investors/trade_history/create')
async def create_trade_history(db: db_dependency):

    try:
        result = db.query(user_model.TradeHistory).all()
        return {'message': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the investors! {e}")


@app.patch('/user/login/')
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


@app.patch('/user/change_name/')
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


@app.patch('/user/block/')
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

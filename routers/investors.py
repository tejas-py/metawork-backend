from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from connection.database import SessionLocal, engine
from models import user_model


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_model.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]
investors_router = APIRouter()


@investors_router.get('/investments')
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


@investors_router.get('/wlb')
async def investor_investments(user_id: str, db: db_dependency):

    try:
        genopets = db.query(user_model.GenopetsWallet).filter(user_model.GenopetsWallet.user_id == user_id).first()
        star_atlas = db.query(user_model.StarAtlasWallet).filter(user_model.StarAtlasWallet.user_id == user_id).first()
        synesis_one = db.query(user_model.SynesisOneWallet).filter(user_model.SynesisOneWallet.user_id == user_id).first()

        return {'genopets': genopets, 'star_atlas': star_atlas, 'synesis_one': synesis_one}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the investments! {e}")


@investors_router.get('/trade_history')
async def investors_trade_history(db: db_dependency):

    try:
        result = db.query(user_model.TradeHistory).all()
        return {'message': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the investors trade history! {e}")


@investors_router.post('/trade_history/create')
async def create_trade_history(db: db_dependency):

    try:
        result = db.query(user_model.TradeHistory).all()
        return {'message': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the investors! {e}")


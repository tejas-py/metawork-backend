from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session

import utils.CommonFunctions
from connection.database import SessionLocal, engine
from models import investor_model
import Validators

# Configure app
app = FastAPI()
investor_model.Base.metadata.create_all(bind=engine)
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
    return RedirectResponse("https://metawork.securetool.company", status_code=302)


@app.post('/user/investor/create/')
async def create_investor(details: Validators.create_investor_validator.InvestorBase, db: db_dependency):
    # Get today seconds
    today_epoch_time = utils.CommonFunctions.today_seconds()

    # Create the investors table
    db_investors = investor_model.Investors(
        token_id=details.token_id,
        wallet_address=details.wallet_address,
        registration_date_time=today_epoch_time,
        last_online=details.last_online,
        total_investments=details.total_investments,
        total_withdrawn=details.total_withdrawn
    )
    db.add(db_investors)
    db.commit()
    db.refresh(db_investors)

    # create holdings table
    for asset_balance in details.holding:
        db_holding = investor_model.Holdings(
            asset_id=asset_balance.asset_id,
            balance=asset_balance.balance,
            investors_id=db_investors.token_id
        )
        db.add(db_holding)
    db.commit()
    db.refresh(db_investors)

    # Create the yield table
    for dividend in details.total_yield:
        db_dividend = investor_model.TotalYield(
            amount=dividend.amount,
            investors_id=db_investors.token_id
        )
        db.add(db_dividend)
    db.commit()
    db.refresh(db_investors)

    # create the trade history table
    for trade in details.trade_history:
        db_trade = investor_model.TradeHistory(
            number=trade.number,
            investors_id=db_investors.token_id
        )
        db.add(db_trade)
    db.commit()
    db.refresh(db_investors)

    return {'message': 'Success'}


@app.get('/user/investor/')
async def investor_details(token_id: int, db: db_dependency):

    if not token_id:
        raise HTTPException(status_code=500, detail="token_id missing")

    try:
        result = db.query(investor_model.Investors).filter(investor_model.Investors.token_id == token_id).first()
        if not result:
            return HTTPException(status_code=404, detail="User Not found")
        return {'message': result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to found the user! {e}")


@app.patch('/user/investor/login/')
async def investor_login(payload: Validators.login_investor_validator.LoginInvestor, db: db_dependency):
    if not payload:
        raise HTTPException(status_code=500, detail="token_id missing")
    try:
        investor_db = db.query(investor_model.Investors.filter(investor_model.Investors.token_id == payload.token_id)
                               .first())

        investor_db.last_online = utils.CommonFunctions.today_seconds()
        db.add(investor_db)
        db.commit()
        db.refresh(investor_db)
        return {'message': investor_db}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to login the user! {e}")


@app.patch('/user/investor/block/')
async def login_investor(payload: Validators.block_investor_validator.BlockInvestor, db: db_dependency):
    if not payload:
        raise HTTPException(status_code=500, detail="token_id missing")
    try:
        investor_db = db.query(investor_model.Investors.filter(investor_model.Investors.token_id == payload.token_id)
                               .first())

        investor_db.blocked = payload.block
        db.add(investor_db)
        db.commit()
        db.refresh(investor_db)
        return {'message': investor_db}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error! Not able to login the user! {e}")
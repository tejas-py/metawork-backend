from sqlalchemy import Column, String, Integer
from connection.database import Base


class MetaworkAssets(Base):
    __tablename__ = 'metawork_assets'

    asset_name = Column(String,primary_key=True, index=True, unique=True)
    token = Column(String, index=True)
    asset_symbol = Column(String, unique=True)
    blockchain_network = Column(String)
    url = Column(String, unique=True)
    total_investors = Column(Integer)
    total_metaworkers = Column(Integer)
    total_investments = Column(Integer)

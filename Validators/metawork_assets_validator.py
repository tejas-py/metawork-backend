from pydantic import BaseModel


class MetaworkAssetsBase(BaseModel):
    asset_name: str
    token: str
    asset_symbol: str
    blockchain_network: str
    url: str
    total_investors: str
    total_metaworkers: int
    total_investments: int

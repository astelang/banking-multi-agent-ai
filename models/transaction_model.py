from pydantic import BaseModel

class Transaction(BaseModel):

    amount: float
    country: str
    account_age: int
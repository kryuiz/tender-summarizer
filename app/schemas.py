from pydantic import BaseModel


class TenderSummary(BaseModel):
    contract_amount: str
    deadline: str
    requirements: list[str]
    penalties: list[str]

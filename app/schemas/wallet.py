import uuid
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, field_validator


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperationRequest(BaseModel):
    operation_type: OperationType
    amount: Decimal

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("amount must be positive")
        return v


class WalletResponse(BaseModel):
    id: uuid.UUID
    balance: Decimal

    model_config = {"from_attributes": True}


class ErrorResponse(BaseModel):
    detail: str

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.wallet import (
    ErrorResponse,
    WalletOperationRequest,
    WalletResponse,
)
from app.services.wallet_service import (
    InsufficientFundsError,
    WalletNotFoundError,
    WalletService,
)

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post(
    "/{wallet_uuid}/operation",
    response_model=WalletResponse,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def wallet_operation(
    wallet_uuid: uuid.UUID,
    payload: WalletOperationRequest,
    db: AsyncSession = Depends(get_db),
) -> WalletResponse:
    service = WalletService(db)
    try:
        wallet = await service.perform_operation(
            wallet_id=wallet_uuid,
            operation_type=payload.operation_type,
            amount=payload.amount,
        )
    except WalletNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InsufficientFundsError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    return WalletResponse.model_validate(wallet)


@router.get(
    "/{wallet_uuid}",
    response_model=WalletResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_wallet(
    wallet_uuid: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> WalletResponse:
    service = WalletService(db)
    try:
        wallet = await service.get_wallet(wallet_uuid)
    except WalletNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return WalletResponse.model_validate(wallet)

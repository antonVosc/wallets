import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet
from app.schemas.wallet import OperationType


class InsufficientFundsError(Exception):
    pass


class WalletNotFoundError(Exception):
    pass


class WalletService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_wallet(self, wallet_id: uuid.UUID) -> Wallet:
        result = await self.db.execute(
            select(Wallet).where(Wallet.id == wallet_id)
        )
        wallet = result.scalar_one_or_none()
        if wallet is None:
            raise WalletNotFoundError(
                f"Wallet {wallet_id} not found"
            )
        return wallet

    async def perform_operation(
        self,
        wallet_id: uuid.UUID,
        operation_type: OperationType,
        amount: Decimal,
    ) -> Wallet:
        # SELECT ... FOR UPDATE prevents concurrent balance corruption
        result = await self.db.execute(
            select(Wallet)
            .where(Wallet.id == wallet_id)
            .with_for_update()
        )
        wallet = result.scalar_one_or_none()

        if wallet is None:
            raise WalletNotFoundError(
                f"Wallet {wallet_id} not found"
            )

        if operation_type == OperationType.DEPOSIT:
            wallet.balance += amount
        elif operation_type == OperationType.WITHDRAW:
            if wallet.balance < amount:
                raise InsufficientFundsError(
                    "Insufficient funds for withdrawal"
                )
            wallet.balance -= amount

        await self.db.commit()
        await self.db.refresh(wallet)
        return wallet

    async def create_wallet(
        self, wallet_id: uuid.UUID | None = None
    ) -> Wallet:
        wallet = Wallet(
            id=wallet_id or uuid.uuid4(),
            balance=Decimal("0"),
        )
        self.db.add(wallet)
        await self.db.commit()
        await self.db.refresh(wallet)
        return wallet

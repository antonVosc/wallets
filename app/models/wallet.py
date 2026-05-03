import uuid

from sqlalchemy import Numeric, Column
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    balance = Column(Numeric(precision=20, scale=2), nullable=False, default=0)
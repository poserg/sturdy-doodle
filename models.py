import enum
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, \
    Text, BigInteger, Enum, Numeric
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class AssetType(enum.Enum):
    BOND = 1
    STOCK = 2


class Asset(Base):
    __tablename__ = "asset"
    ticker = Column(String(20), primary_key=True)
    name = Column(String)
    type = Column(Enum('BOND', 'STOCK', 'CASH'), nullable=False)
    amount = Column(BigInteger, nullable=False, default=0)
    shares_in_lot = Column(BigInteger, nullable=False, default=1)

    def __repr__(self):
        return f"Asset(ticker={self.ticker!r}, name={self.name!r}, type={self.type!r}, amount={self.amount!r})"


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(BigInteger, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    credit_ticker = Column(String(20), ForeignKey(
        'asset.ticker'), nullable=False)
    credit = relationship(
        'Asset', primaryjoin='Transaction.credit_ticker == Asset.ticker')

    debit_ticker = Column(String(20), ForeignKey(
        'asset.ticker'), nullable=False)
    debit = relationship(
        'Asset', primaryjoin='Transaction.debit_ticker == Asset.ticker')

    price = Column(Numeric, nullable=False)

    def __repr__(self):
        return f"Transaction(datetime={self.datetime}, credit={self.credit.ticker}, debit={self.debit.ticker}, price={self.price})"

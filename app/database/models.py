import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    language = Column(String(5), default="ru")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    listings = relationship("Listing", back_populates="seller")
    purchases = relationship("Order", foreign_keys="Order.buyer_id", back_populates="buyer")
    sales = relationship("Order", foreign_keys="Order.seller_id", back_populates="seller")
    transactions = relationship("Transaction", back_populates="user")
    payouts = relationship("Payout", back_populates="user")

class Listing(Base):
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"))
    price = Column(Float, nullable=False)
    level = Column(Integer, nullable=False)
    server = Column(String(50), nullable=False)
    inventory = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(30), default="pending_review") # pending_review, active, reserved, sold, rejected
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    seller = relationship("User", back_populates="listings")
    images = relationship("ListingImage", back_populates="listing", cascade="all, delete-orphan")
    order = relationship("Order", back_populates="listing", uselist=False)

class ListingImage(Base):
    __tablename__ = "listing_images"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    file_id = Column(String(255), nullable=False)
    
    listing = relationship("Listing", back_populates="images")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))
    price = Column(Float, nullable=False)
    commission = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(30), default="pending_payment") # pending_payment, paid, transfer_pending, verification, completed, disputed, refunded
    transfer_info = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    listing = relationship("Listing", back_populates="order")
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="purchases")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="sales")
    payment = relationship("Payment", back_populates="order", uselist=False)
    dispute = relationship("Dispute", back_populates="order", uselist=False)

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    provider_payment_id = Column(String(255), unique=True, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String(30), default="pending") # pending, verified, refunded
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    order = relationship("Order", back_populates="payment")

class Payout(Base):
    __tablename__ = "payouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    status = Column(String(30), default="requested") # requested, approved, rejected, completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="payouts")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    type = Column(String(30), nullable=False) # SALE, COMMISSION, PAYOUT, REFUND, ADJUSTMENT
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="transactions")

class Dispute(Base):
    __tablename__ = "disputes"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))
    reason = Column(Text, nullable=False)
    evidence = Column(Text, nullable=True)
    status = Column(String(30), default="active") # active, resolved_refund, resolved_release
    admin_decision = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    order = relationship("Order", back_populates="dispute")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Settings(Base):
    __tablename__ = "settings"
    
    key = Column(String(50), primary_key=True)
    value = Column(String(255), nullable=False)

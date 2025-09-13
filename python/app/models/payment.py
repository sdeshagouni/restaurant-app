"""
Payment models for payment gateway and transaction management.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Integer, ForeignKey, Text, JSON
from sqlalchemy import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal

from app.models.base import BaseModel, PaymentStatus, PaymentMethod, GatewayProvider


class PaymentGateway(BaseModel):
    """Payment gateway configuration."""
    __tablename__ = "payment_gateway"
    
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    gateway_name = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)
    api_key = Column(String(255), nullable=True)
    secret_key = Column(String(255), nullable=True)
    webhook_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_test_mode = Column(Boolean, default=True, nullable=False)
    configuration = Column(JSON, nullable=True)
    
    restaurant = relationship("Restaurant", back_populates="payment_gateways")
    transactions = relationship("PaymentTransaction", back_populates="gateway", cascade="all, delete-orphan")


class PaymentTransaction(BaseModel):
    """Payment transaction model."""
    __tablename__ = "payment_transaction"
    
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False, index=True)
    gateway_id = Column(UUID(as_uuid=True), ForeignKey("payment_gateway.id"), nullable=False, index=True)
    
    transaction_id = Column(String(255), nullable=False, unique=True, index=True)
    gateway_transaction_id = Column(String(255), nullable=True)
    payment_method = Column(String(50), nullable=False, default=PaymentMethod.CARD)
    payment_status = Column(String(20), nullable=False, default=PaymentStatus.PENDING)
    
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    gateway_fee = Column(Numeric(8, 2), nullable=True)
    net_amount = Column(Numeric(10, 2), nullable=True)
    
    gateway_response = Column(JSON, nullable=True)
    failure_reason = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    order = relationship("Order", back_populates="payment_transactions")
    gateway = relationship("PaymentGateway", back_populates="transactions")
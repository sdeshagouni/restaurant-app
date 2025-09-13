"""
Payment processing API routes.
Handles payment gateways and transaction processing.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from uuid import UUID
from decimal import Decimal

from app.core.security import get_staff_user, get_owner_or_manager_user, get_restaurant_context
from app.models.payment import PaymentGateway, PaymentTransaction
from app.models.order import Order
from app.models.base import PaymentMethod, PaymentStatus
from app.core.database import get_db

router = APIRouter()


@router.post("/orders/{order_id}/payment-intent", response_model=Dict[str, Any])
async def create_payment_intent(
    order_id: UUID,
    payment_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Create payment intent."""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Get default payment gateway for restaurant
    gateway = db.query(PaymentGateway).filter(
        PaymentGateway.restaurant_id == order.restaurant_id,
        PaymentGateway.is_default == True,
        PaymentGateway.status == "active"
    ).first()
    
    if not gateway:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active payment gateway found"
        )
    
    # Create payment intent (mock implementation)
    payment_intent_id = f"pi_{order.id}_{''.join(str(order.id).split('-')[:2])}"
    
    return {
        "success": True,
        "data": {
            "payment_intent": {
                "id": payment_intent_id,
                "client_secret": f"{payment_intent_id}_secret_xyz",
                "amount": float(order.total_amount),
                "currency": "USD",
                "status": "requires_payment_method",
                "payment_url": f"https://checkout.stripe.com/pay/{payment_intent_id}"
            }
        }
    }


@router.post("/orders/{order_id}/payment/cash", response_model=Dict[str, Any])
async def process_cash_payment(
    order_id: UUID,
    payment_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user = Depends(get_staff_user)
):
    """Process cash payment (Staff)."""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Verify staff has access to this restaurant
    get_restaurant_context(order.restaurant_id, current_user)
    
    amount_paid = Decimal(str(payment_data.get("amount_paid", 0)))
    change_given = Decimal(str(payment_data.get("change_given", 0)))
    
    # Create payment transaction
    transaction = PaymentTransaction(
        restaurant_id=order.restaurant_id,
        order_id=order.id,
        internal_reference=f"CASH_{order.order_number}_{order.id}",
        payment_method=PaymentMethod.CASH,
        amount=order.total_amount,
        net_amount=order.total_amount,
        status=TransactionStatus.COMPLETED,
        customer_name=order.guest_name
    )
    
    db.add(transaction)
    
    # Update order payment status
    from app.models.base import PaymentStatus
    order.payment_status = PaymentStatus.PAID
    order.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "data": {
            "transaction": {
                "id": str(transaction.id),
                "internal_reference": transaction.internal_reference,
                "payment_method": transaction.payment_method,
                "amount": float(transaction.amount),
                "status": transaction.status,
                "completed_at": transaction.created_at.isoformat() + "Z"
            },
            "order": {
                "id": str(order.id),
                "payment_status": order.payment_status,
                "amount_paid": float(amount_paid),
                "change_given": float(change_given)
            }
        },
        "message": "Cash payment processed successfully"
    }


from datetime import datetime
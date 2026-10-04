import uuid

class PaymentProvider:
    async def create_payment(self, amount: float, order_id: int) -> dict:
        raise NotImplementedError
        
    async def verify_payment(self, payment_id: str) -> bool:
        raise NotImplementedError
        
    async def refund_payment(self, payment_id: str) -> bool:
        raise NotImplementedError
        
    async def create_payout(self, amount: float, recipient_info: str) -> bool:
        raise NotImplementedError

class MockPaymentProvider(PaymentProvider):
    async def create_payment(self, amount: float, order_id: int) -> dict:
        payment_id = f"mock_pay_{uuid.uuid4().hex[:10]}"
        return {
            "payment_id": payment_id,
            "pay_url": f"https://t.me/mock_pay_bot?start=pay_{payment_id}",
            "amount": amount
        }
        
    async def verify_payment(self, payment_id: str) -> bool:
        # In mock system, payment is verified successfully
        return True
        
    async def refund_payment(self, payment_id: str) -> bool:
        return True
        
    async def create_payout(self, amount: float, recipient_info: str) -> bool:
        return True

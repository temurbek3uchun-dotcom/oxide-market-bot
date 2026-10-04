from app.config import COMMISSION_PERCENT, MIN_COMMISSION

def calculate_commission(price: float) -> tuple[float, float]:
    """
    Calculates marketplace commission and seller net amount.
    Returns: (commission_amount, seller_amount)
    """
    calculated = price * (COMMISSION_PERCENT / 100.0)
    commission = max(calculated, float(MIN_COMMISSION))
    if commission > price:
        commission = price
    seller_amount = price - commission
    return round(commission, 2), round(seller_amount, 2)

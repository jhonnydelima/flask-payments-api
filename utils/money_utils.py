from decimal import Decimal, ROUND_HALF_UP

def to_small_unit(amount: Decimal) -> int:
  return int((amount * 100).to_integral_value(rounding=ROUND_HALF_UP))

def from_small_unit(amount: int) -> float:
  return float(Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) / 100)
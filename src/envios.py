"""Tarifas de envio con politicas de zona independientes."""
import math
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


WEIGHT_MIN_EXCLUSIVE = 0
WEIGHT_MAX_KG = 50
L1_KG = 3
L2_KG = 10
TARIFF_UP_TO_L1 = 6000
TARIFF_UP_TO_L2 = 9000
PRICE_PER_KG_OVER_L2 = 800
RURAL_SURCHARGE = 0.20
NATIONAL_SURCHARGE = 0.50
INSULAR_SURCHARGE = 0.70
FREQUENT_DISCOUNT = 0.05
VIP_DISCOUNT = 0.15
COUPON_DISCOUNT = 0.10
WEEKEND_DAYS = (6, 7)
WEEKEND_SURCHARGE = 2000
MINIMUM_PRICE = 5000
ROUNDING_UNIT = 100
VALID_ZONES = ("urbana", "rural", "nacional", "insular")


class ZonePolicy:
    """Policy for calculating the zone surcharge."""

    def apply(self, price):
        return price


@dataclass(frozen=True)
class PercentageSurcharge(ZonePolicy):
    rate: float

    def apply(self, price):
        return price * (1 + self.rate)


ZONE_POLICIES = {
    "urbana": ZonePolicy(),
    "rural": PercentageSurcharge(RURAL_SURCHARGE),
    "nacional": PercentageSurcharge(NATIONAL_SURCHARGE),
    "insular": PercentageSurcharge(INSULAR_SURCHARGE),
}


def _validate_input(weight, zone, day):
    if (
        isinstance(weight, bool)
        or not isinstance(weight, (int, float))
        or not math.isfinite(weight)
        or not WEIGHT_MIN_EXCLUSIVE < weight <= WEIGHT_MAX_KG
    ):
        raise ValueError("peso inv\u00e1lido")
    if zone not in VALID_ZONES:
        raise ValueError("zona inv\u00e1lida")
    if type(day) is not int or not 1 <= day <= 7:
        raise ValueError("dia invalido")


def _base_tariff(weight):
    if weight <= L1_KG:
        return TARIFF_UP_TO_L1
    if weight <= L2_KG:
        return TARIFF_UP_TO_L2
    return TARIFF_UP_TO_L2 + (weight - L2_KG) * PRICE_PER_KG_OVER_L2


def _apply_customer_discount(price, customer):
    rates = {"frecuente": FREQUENT_DISCOUNT, "vip": VIP_DISCOUNT}
    return price * (1 - rates.get(customer, 0))


def _apply_coupon_discount(price, zone, coupon):
    if zone != "insular" and coupon == "ENVIO10":
        return price * (1 - COUPON_DISCOUNT)
    return price


def _round_to_hundred(price):
    hundreds = (Decimal(str(price)) / Decimal(ROUNDING_UNIT)).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    return int(hundreds * ROUNDING_UNIT)


def calculate_shipping_cost(weight, zone, customer, day, coupon=None):
    """Calculate total shipping cost according to R1-R9."""
    _validate_input(weight, zone, day)
    price = ZONE_POLICIES[zone].apply(_base_tariff(weight))
    if day in WEEKEND_DAYS:
        price += WEEKEND_SURCHARGE
    price = _apply_customer_discount(price, customer)
    price = _apply_coupon_discount(price, zone, coupon)
    return _round_to_hundred(max(price, MINIMUM_PRICE))
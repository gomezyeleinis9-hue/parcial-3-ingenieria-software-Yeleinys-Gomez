# envios.py - c?digo heredado, versi?n 1.0.0
import math
from decimal import Decimal, ROUND_HALF_UP

CONFIG = {
    "L1": 3,
    "L2": 10,
    "RECARGO_RURAL": 0.20,
    "RECARGO_NACIONAL": 0.50,
    "RECARGO_INSULAR": 0.70,
    "DESC_VIP": 0.15,
    "RECARGO_FINDE": 2000,
}

def calc(p, z, c, d, cup=None, flag=False):
    if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or p <= 0 or p > 50:
        raise ValueError("peso inv\u00e1lido")
    if type(d) is not int or not 1 <= d <= 7:
        raise ValueError("dia invalido")
    if z not in ("urbana", "rural", "nacional", "insular"):
        raise ValueError("zona inv\u00e1lida")
    if p <= CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "urbana":
        t = t
    elif z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    elif z == "insular":
        t = t + t * CONFIG["RECARGO_INSULAR"]
    # fin de semana
    if d >= 6:
        t = t + CONFIG["RECARGO_FINDE"]
    if c == "frecuente":
        t = t - t * 0.05
    if c == "vip":
        t = t - t * CONFIG["DESC_VIP"]
    if cup is not None and z != "insular":
        if cup == "ENVIO10":
            t = t - t * 0.10
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    centenas = (Decimal(str(t)) / Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(centenas * 100)

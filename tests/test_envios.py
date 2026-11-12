"""Suite de caja negra para R1-R9 del cotizador EnvíaYa."""
import re

import pytest

from src.envios import calculate_shipping_cost


CASES = [
    pytest.param((-0.01, "urbana", "normal", 1, None), ("ValueError", "peso inválido"), id="BB-01"),
    pytest.param((0, "urbana", "normal", 1, None), ("ValueError", "peso inválido"), id="BB-02"),
    pytest.param((0.01, "urbana", "normal", 1, None), 6000, id="BB-03"),
    pytest.param((2.99, "urbana", "normal", 1, None), 6000, id="BB-04"),
    pytest.param((3, "urbana", "normal", 1, None), 6000, id="BB-05"),
    pytest.param((3.01, "urbana", "normal", 1, None), 9000, id="BB-06"),
    pytest.param((9.99, "urbana", "normal", 1, None), 9000, id="BB-07"),
    pytest.param((10, "urbana", "normal", 1, None), 9000, id="BB-08"),
    pytest.param((10.01, "urbana", "normal", 1, None), 9000, id="BB-09"),
    pytest.param((10.0625, "urbana", "normal", 1, None), 9100, id="BB-10"),
    pytest.param((50, "urbana", "normal", 1, None), 41000, id="BB-11"),
    pytest.param((50.01, "urbana", "normal", 1, None), ("ValueError", "peso inválido"), id="BB-12"),
    pytest.param((4, "exterior", "normal", 2, None), ("ValueError", None), id="BB-13"),
    pytest.param((4, "urbana", "normal", 0, None), ("ValueError", None), id="BB-14"),
    pytest.param((10, "urbana", "normal", 6, None), 11000, id="BB-15"),
    pytest.param((10, "urbana", "normal", 7, None), 11000, id="BB-16"),
    pytest.param((10, "urbana", "normal", 5, None), 9000, id="BB-17"),
    pytest.param((3, "rural", "normal", 1, None), 7200, id="BB-18"),
    pytest.param((3, "nacional", "normal", 1, None), 9000, id="BB-19"),
    pytest.param((10, "urbana", "frecuente", 1, None), 8600, id="BB-20"),
    pytest.param((10, "urbana", "vip", 1, None), 7700, id="BB-21"),
    pytest.param((10, "urbana", "normal", 1, "ENVIO10"), 8100, id="BB-22"),
    pytest.param((10, "urbana", "frecuente", 1, "ENVIO10"), 7700, id="BB-23"),
    pytest.param((10, "urbana", "vip", 1, "ENVIO10"), 6900, id="BB-24"),
    pytest.param((10, "urbana", "vip", 1, "OTRO"), 7700, id="BB-25"),
    pytest.param((0.01, "urbana", "vip", 1, "ENVIO10"), 5000, id="BB-26"),
    pytest.param((10.5, "urbana", "normal", 1, None), 9400, id="BB-27"),
    pytest.param((10, "urbana", "normal", 8, None), ("ValueError", None), id="BB-28"),
    pytest.param(("no-numérico", "urbana", "normal", 1, None), ("ValueError", None), id="BB-29"),
    pytest.param((10, "urbana", "normal", 6.5, None), ("ValueError", None), id="BB-30"),
    pytest.param((9.5, "nacional", "frecuente", 7, "ENVIO10"), 13300, id="BB-31"),
    pytest.param((49.99, "urbana", "normal", 1, None), 41000, id="BB-32"),
]


@pytest.mark.parametrize("args, expected", CASES)
def test_matriz_caja_negra(args, expected):
    if isinstance(expected, tuple) and expected[0] == "ValueError":
        if expected[1] is None:
            with pytest.raises(ValueError):
                calculate_shipping_cost(*args)
        else:
            with pytest.raises(ValueError, match=re.escape(expected[1])):
                calculate_shipping_cost(*args)
    else:
        assert calculate_shipping_cost(*args) == expected


INSULAR_CASES = [
    pytest.param((10, "insular", "normal", 1, None), 15300, id="IN-01"),
    pytest.param((10, "insular", "normal", 6, None), 17300, id="IN-02"),
    pytest.param((10, "insular", "normal", 1, "ENVIO10"), 15300, id="IN-03"),
    pytest.param((51, "insular", "normal", 1, None), ("ValueError", "peso inv" + chr(0xE1) + "lido"), id="IN-04"),
    pytest.param((10, "exterior", "normal", 1, None), ("ValueError", None), id="IN-05"),
]


@pytest.mark.parametrize("args, expected", INSULAR_CASES)
def test_regla_r9_zona_insular(args, expected):
    if isinstance(expected, tuple) and expected[0] == "ValueError":
        if expected[1] is None:
            with pytest.raises(ValueError):
                calculate_shipping_cost(*args)
        else:
            with pytest.raises(ValueError, match=re.escape(expected[1])):
                calculate_shipping_cost(*args)
    else:
        assert calculate_shipping_cost(*args) == expected

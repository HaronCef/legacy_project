# tests for CR-313: duplicated calculate_growth* in analytics.py
from src.analytics import (calculate_growth, calculate_growth_yoy,
                           calculate_growth_mom, calculate_growth_wow)


def test_all_growth_functions_identical():
    assert calculate_growth(120, 100) == calculate_growth_yoy(120, 100)
    assert calculate_growth(120, 100) == calculate_growth_mom(120, 100)
    assert calculate_growth(120, 100) == calculate_growth_wow(120, 100)


def test_growth_values_same_as_before():
    assert calculate_growth(120, 100) == 20.0
    assert calculate_growth_yoy(80, 100) == -20.0
    assert calculate_growth_mom(50, 0) == 100.0
    assert calculate_growth_wow(0, 0) == 0.0

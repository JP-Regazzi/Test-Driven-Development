# test_checkout.py

import pytest
from checkout import Checkout

def test_create_instance():
    checkout = Checkout()
    assert isinstance(checkout, Checkout)

import pytest
from checkout import Checkout

def test_set_price():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    # Test that the price is stored correctly
    assert checkout.prices["toothpaste"] == 1.0

def test_add_item():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)  # Prerequisite for adding an item
    checkout.add_item("toothpaste")
    # Test that the item count in the basket is incremented
    assert checkout.basket["toothpaste"] == 1

def test_set_price_and_add_item():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.add_item("toothpaste")
    assert checkout.basket["toothpaste"] == 1

def test_total_calculation_single_item():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.add_item("toothpaste")
    assert checkout.total() == 1.0

def test_total_calculation_multiple_items():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.set_price("pinaple", 0.5)
    checkout.add_item("toothpaste")
    checkout.add_item("toothpaste")
    checkout.add_item("pinaple")
    # Expected: 1.0 * 2 + 0.5 * 1 = 2.5
    assert checkout.total() == 2.5

def test_discount_rule_application():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    # Set a discount rule: if at least 2 toothpaste, apply 10% discount.
    checkout.add_discount_rule("toothpaste", 2, 0.10)
    checkout.add_item("toothpaste")
    checkout.add_item("toothpaste")
    # Expected: 1.0 * 2 * 0.90 = 1.8
    assert checkout.total() == pytest.approx(1.8)

def test_discount_rule_not_applied_if_quantity_not_met():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.add_discount_rule("toothpaste", 3, 0.10)
    checkout.add_item("toothpaste")
    checkout.add_item("toothpaste")
    # Discount rule not triggered because quantity (2) is less than required (3).
    assert checkout.total() == 2.0

def test_exception_when_item_without_price():
    checkout = Checkout()
    with pytest.raises(ValueError):
        checkout.add_item("shampoo")

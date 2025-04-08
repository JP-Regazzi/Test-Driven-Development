import pytest
from checkout import Checkout

def test_create_instance():
    checkout = Checkout()
    assert isinstance(checkout, Checkout)
    print("\n.✅ test_create_instance passed")

def test_set_price():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    assert checkout.prices["toothpaste"] == 1.0
    print("✅ test_set_price passed")

def test_add_item():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.add_item("toothpaste")
    assert checkout.basket["toothpaste"] == 1
    print("✅ test_add_item passed")

def test_set_price_and_add_item():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.add_item("toothpaste")
    assert checkout.basket["toothpaste"] == 1
    print("✅ test_set_price_and_add_item passed")

def test_total_calculation_single_item():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.add_item("toothpaste")
    assert checkout.total() == 1.0
    print("✅ test_total_calculation_single_item passed")

def test_total_calculation_multiple_items():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.set_price("pinaple", 0.5)
    checkout.add_item("toothpaste")
    checkout.add_item("toothpaste")
    checkout.add_item("pinaple")
    assert checkout.total() == 2.5
    print("✅ test_total_calculation_multiple_items passed")

def test_discount_rule_application():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.add_discount_rule("toothpaste", 2, 0.10)
    checkout.add_item("toothpaste")
    checkout.add_item("toothpaste")
    assert checkout.total() == pytest.approx(1.8)
    print("✅ test_discount_rule_application passed")

def test_discount_rule_not_applied_if_quantity_not_met():
    checkout = Checkout()
    checkout.set_price("toothpaste", 1.0)
    checkout.add_discount_rule("toothpaste", 3, 0.10)
    checkout.add_item("toothpaste")
    checkout.add_item("toothpaste")
    assert checkout.total() == 2.0
    print("✅ test_discount_rule_not_applied_if_quantity_not_met passed")

def test_exception_when_item_without_price():
    checkout = Checkout()
    with pytest.raises(ValueError):
        checkout.add_item("shampoo")
    print("✅ test_exception_when_item_without_price passed")

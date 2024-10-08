import pytest
from products import Product

def test_create_normal_product():
    """Test that creating a normal product works."""
    product = Product(name="MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.get_quantity() == 100
    assert product.is_active()


def test_create_product_invalid_details():
    """Test for invalid details (empty name, negative price) invokes an exception."""
    try:
        Product(name="", price=1450, quantity=100)
        assert False, "Expected ValueError for empty product name, but no exception was raised."
    except ValueError:
        assert True, "Raised ValueError as expected for empty product name."

    try:
        Product(name="MacBook Air M2", price=-1450, quantity=100)
        assert False, "Expected ValueError for negative price, but no exception was raised."
    except ValueError:
        assert True, "Raised ValueError as expected for negative price."


def test_product_becomes_inactive_at_zero_quantity():
    """Test that when a product reaches 0 quantity, it becomes inactive."""
    product = Product(name="MacBook Air M2", price=1450, quantity=1)
    product.buy(1)
    assert product.get_quantity() == 0
    assert not product.is_active()  # Product should be inactive when quantity is 0


def test_product_purchase_modifies_quantity():
    """Test that product purchase modifies the quantity and returns the right output."""
    product = Product(name="MacBook Air M2", price=1450, quantity=100)
    cost = product.buy(10)
    assert product.get_quantity() == 90  # Quantity should decrease by the purchased amount
    assert cost == 1450 * 10  # The cost should be price * quantity


def test_buy_larger_quantity_invokes_exception():
    """Test that buying a larger quantity than exists invokes exception."""
    product = Product(name="MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        product.buy(10)  # Buying more than available quantity should raise an exception

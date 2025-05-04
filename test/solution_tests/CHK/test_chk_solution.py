import pytest

from lib.solutions.CHK.checkout_solution import CheckoutSolution


@pytest.mark.parametrize(
    "skus,expected",
    [
        # Invalid inputs
        (None, -1),
        ("a", -1),
        ("X", -1),
        ("ABCa", -1),
        # Empty basket
        ("", 0),
        # Single SKUs
        ("A", 50),
        ("B", 30),
        ("C", 20),
        ("D", 15),
        ("E", 40),
        ("F", 10),
        # Multiples of same SKU
        ("AA", 100),
        ("BB", 45),
        ("CC", 40),
        ("DD", 30),
        ("EE", 80),
        ("FF", 20),
        # Special offers for A
        ("AAA", 130),
        ("AAAA", 180),
        ("AAAAA", 200),
        ("AAAAAA", 250),  # 5A for 200 + 1A for 50
        ("AAAAAAA", 300),  # 5A for 200 + 2A for 100
        ("AAAAAAAA", 330),  # 5A for 200 + 3A for 130
        # Special offers for B
        ("BB", 45),
        ("BBB", 75),  # 2B for 45 + 1B for 30
        # Free B with E offer
        ("EEB", 80),  # 2E for 80 + 1B free (not charged)
        ("EEBB", 110),  # 2E for 80 + 1B free + 1B charged (30)
        ("EEEEBB", 160),  # 4E for 160 + 2B free (not charged)
        ("EEEB", 120),  # 3E(120) and B is free
        # Interaction between E and B offers
        ("EEBBB", 125),  # 2E(80) + 3B where 1 is free, so 2B with offer = 45
        # 2F get one F free offer
        ("FF", 20),  # 2F for 20
        ("FFF", 20),  # 3F, but one is free, so paying for 2F = 20
        ("FFFF", 30),  # 4F = 2F for 20 + 2F for 10 (one free)
        ("FFFFF", 40),  # 5F = 2F for 20 + 2F for 20, the 5th costs 0
        ("FFFFFF", 40),  # 6F = 2 sets of 3F, where each set is 2F paid + 1F free
        # Complex combinations
        ("ABCDE", 155),  # A(50) + B(30) + C(20) + D(15) + E(40)
        ("ABCDEF", 165),  # A(50) + B(30) + C(20) + D(15) + E(40) + F(10)
        ("AAAAAEEBAAABB", 455),  # 10A for 400 + 2E for 80 + 3B where 1 is free = 455
        (
            "ABCDECBAABCABBAEEE",
            510,
        ),  # 5A(200) + 5B(105 after discount) + 3C(60) + 2D(30) + 3E(120) - 15 = 510
        (
            "ABCDECBAABCABBAEEEFFFFFFFF",
            570,
        ),  # Previous case (510) + 6F where 2 are free (60) = 570
    ],
)
def test_checkout_with_params(skus, expected):
    """
    Test the checkout functionality with various combinations of items and offers.

    This test covers:
    - Invalid input handling
    - Basic item pricing
    - Multi-item price offers (e.g., 3A for 130)
    - 'Buy X get Y free' offers (e.g., buy 2E get 1B free)
    - 'Buy X get X free' offers (e.g., buy 2F get 1F free)
    - Combined offers
    """
    checkout = CheckoutSolution()
    assert checkout.checkout(skus) == expected

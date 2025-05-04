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
        # Single SKUs
        ("A", 50),
        ("B", 30),
        ("C", 20),
        ("D", 15),
        ("E", 40),
        # Multiples of same SKU
        ("AA", 100),
        ("BB", 45),
        ("CC", 40),
        ("DD", 30),
        ("EE", 80),
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
        # Complex combinations
        ("ABCDE", 155),  # A(50) + B(30) + C(20) + D(15) + E(40)
        ("AAAAAEEBAAABB", 455),  # 10A for 400 + 2E for 80 + 3B where 1 is free = 455
        (
            "ABCDECBAABCABBAEEE",
            510,
        ),  # 5A(200) + 5B(105 after discount) + 3C(60) + 2D(30) + 3E(120) - 15 = 510
    ],
)
def test_checkout_with_params(skus, expected):
    checkout = CheckoutSolution()
    assert checkout.checkout(skus) == expected


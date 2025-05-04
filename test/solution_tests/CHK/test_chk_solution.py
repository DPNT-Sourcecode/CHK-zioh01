import pytest

from lib.solutions.CHK.checkout_solution import CheckoutSolution


@pytest.mark.parametrize(
    "skus,expected",
    [
        # Invalid inputs
        (None, -1),
        ("a", -1),
        ("#", -1),  # Using # as an invalid SKU instead of X
        ("ABC#", -1),
        # Empty basket
        ("", 0),
        # Single SKUs (basic pricing)
        ("A", 50),
        ("B", 30),
        ("C", 20),
        ("D", 15),
        ("E", 40),
        ("F", 10),
        ("G", 20),
        ("H", 10),
        ("I", 35),
        ("J", 60),
        ("K", 70),  # Updated from 80 to 70
        ("L", 90),
        ("M", 15),
        ("N", 40),
        ("O", 10),
        ("P", 50),
        ("Q", 30),
        ("R", 50),
        ("S", 20),  # Updated from 30 to 20
        ("T", 20),
        ("U", 40),
        ("V", 50),
        ("W", 20),
        ("X", 17),  # Updated from 90 to 17
        ("Y", 20),  # Updated from 10 to 20
        ("Z", 21),  # Updated from 50 to 21
        # Multi-price offers for A
        ("AAA", 130),  # 3A for 130
        ("AAAA", 180),  # 3A for 130 + 1A for 50
        ("AAAAA", 200),  # 5A for 200
        ("AAAAAA", 250),  # 5A for 200 + 1A for 50
        ("AAAAAAA", 300),  # 5A for 200 + 2A for 100
        ("AAAAAAAA", 330),  # 5A for 200 + 3A for 130
        # Multi-price offers for B
        ("BB", 45),  # 2B for 45
        ("BBB", 75),  # 2B for 45 + 1B for 30
        # Multi-price offers for H
        ("HHHHH", 45),  # 5H for 45
        ("HHHHHHHHHH", 80),  # 10H for 80
        ("HHHHHHHHHHH", 90),  # 10H for 80 + 1H for 10
        ("HHHHHHHHHHHHHHHH", 135),  # 10H for 80 + 5H for 45 + 1H for 10
        # Multi-price offers for K (updated)
        ("KK", 120),  # 2K for 120 (updated from 150)
        ("KKK", 190),  # 2K for 120 + 1K for 70
        # Multi-price offers for P
        ("PPPPP", 200),  # 5P for 200
        ("PPPPPP", 250),  # 5P for 200 + 1P for 50
        # Multi-price offers for Q
        ("QQQ", 80),  # 3Q for 80
        ("QQQQ", 110),  # 3Q for 80 + 1Q for 30
        # Multi-price offers for V
        ("VV", 90),  # 2V for 90
        ("VVV", 130),  # 3V for 130
        ("VVVV", 180),  # 3V for 130 + 1V for 50
        ("VVVVV", 220),  # 3V for 130 + 2V for 90
        ("VVVVVV", 260),  # 2 sets of 3V for 260
        # Free B with E offer
        ("EEB", 80),  # 2E for 80 + 1B free (not charged)
        ("EEBB", 110),  # 2E for 80 + 1B free + 1B charged (30)
        ("EEEEBB", 160),  # 4E for 160 + 2B free (not charged)
        ("EEEB", 120),  # 3E(120) and B is free
        ("EE", 80),  # 2E for 80, qualify for free B but no B in basket
        # Interaction between E and B offers
        ("EEBBB", 125),  # 2E(80) + 3B where 1 is free = 2B (45)
        # 2F get one F free offer
        ("FF", 20),  # 2F for 20
        ("FFF", 20),  # 3F, but one is free, so paying for 2F = 20
        ("FFFF", 30),  # 4F = 2F for 20 + 2F for 10 (one free)
        ("FFFFF", 40),  # 5F = 2F for 20 + 2F for 20, the 5th costs 0
        ("FFFFFF", 40),  # 6F = 2 sets of 3F, where each set is 2F paid + 1F free
        # Buy 3N get one M free
        ("NNNM", 120),  # 3N(120) + M free
        ("NNNNM", 160),  # 3N(120) + 1N(40) + M free
        ("NNNMM", 135),  # 3N(120) + 1M(15) + 1M free
        ("NNN", 120),  # 3N(120), qualify for free M but no M in basket
        # Buy 3R get one Q free
        ("RRRQ", 150),  # 3R(150) + Q free
        ("RRRQQQ", 210),  # 3R(150) + 2Q(60) + 1Q free
        ("RRR", 150),  # 3R(150), qualify for free Q but no Q in basket
        # Buy 3U get one U free
        ("UUU", 120),  # 3U(120), no free item yet
        ("UUUU", 120),  # 3U(120) + 1U free
        ("UUUUUUU", 240),  # 6U(240) + 1U free
        ("UUUUUUUU", 240),  # 6U(240) + 2U free
        # New group discount offer: any 3 of S,T,X,Y,Z for 45
        ("STX", 45),  # Group offer: any 3 of S,T,X,Y,Z
        ("STY", 45),  # Group offer: any 3 of S,T,X,Y,Z
        ("STZ", 45),  # Group offer: any 3 of S,T,X,Y,Z
        ("XYZ", 45),  # Group offer: any 3 of S,T,X,Y,Z
        ("STXYZ", 82),  # Group offer (STZ) + X + Y
        ("STXY", 62),  # Group offer (STY) + X
        ("SSSSS", 85),  # 1 Group offer (3S) + 2S
        ("STXSTX", 90),  # 2 Group offers
        ("STXSTXY", 107),  # 2 Group offers + Y
        ("SSSTTTYYYZZZ", 180),  # 4 Group offers (from 12 items)
        # Prioritisation of higher priced items in group discount
        ("ZZZ", 45),  # Group offer with 3Z (normally 63)
        ("ZZTXX", 79),  # Group offer with Z,Z,X + T + X
        ("SSTX", 62),  # Group offer with S,T,X + S
        # Complex combinations across multiple offer types
        ("ABCDE", 155),  # A(50) + B(30) + C(20) + D(15) + E(40)
        (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            837,
        ),  # One of each item with all applicable offers
        ("AAAAAEEBAAABB", 455),  # 10A for 400 + 2E for 80 + 3B where 1 is free = 455
        (
            "ABCDECBAABCABBAEEE",
            510,
        ),  # 5A(200) + 5B(105) + 3C(60) + 2D(30) + 3E(120) - 1B free
        ("RRRNNNFFUUU", 410),  # 3R(150) + 3N(120) + 2F(20) + 3U(120) = 410
        ("EEBRRRQQ", 260),  # 2E + B(free) + 3R + Q(free) + Q
        # Comprehensive edge case that tests all three offer types together
        (
            "AAAEEEFFRSTXYZ",
            402,
        ),  # 3A(130) + 2E(80) + 3F(20) + R(50) + S,T,X,Y,Z(122)
        # B from 2E is not present so not applied
        # R doesn't qualify for free Q (need 3R)
        # Group discount selects highest value items (Z,S,T) for 45
        # X(17) and Y(20) charged at normal price
    ],
)
def test_checkout_with_params(skus, expected):
    """
    Test the checkout functionality with various combinations of items and offers.

    This test thoroughly covers:
    - Invalid input handling (None, lowercase letters, invalid characters)
    - Empty basket handling
    - Basic item pricing for all 26 SKUs (A through Z) with updated prices for K, S, X, Y, Z
    - Various multi-item price offers:
      * Different quantities (2B for 45, 3A for 130, 5A for 200, 10H for 80)
      * Multiple offers for same item (A, H, V)
      * Best value application ordering
    - 'Buy X get Y free' offers:
      * Different items (buy 2E get 1B free, buy 3N get 1M free, buy 3R get 1Q free)
      * Interaction with multi-price offers (E and B combination)
      * Edge case: qualifying for free item that's not in basket
    - 'Buy X get X free' offers:
      * Self-referential offers (buy 2F get 1F free, buy 3U get 1U free)
      * Different quantities and patterns
    - Group discount offers:
      * Buy any 3 of S,T,X,Y,Z for 45
      * Prioritisation of higher priced items for maximum customer value
      * Multiple group discount applications
    - Complex combinations across all offer types
    """
    checkout = CheckoutSolution()
    assert checkout.checkout(skus) == expected




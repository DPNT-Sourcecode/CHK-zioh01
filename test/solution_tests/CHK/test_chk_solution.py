from lib.solutions.CHK.checkout_solution import CheckoutSolution


def test_checkout_solution():
    checkout = CheckoutSolution()

    # Invalid inputs
    assert checkout.checkout(None) == -1
    assert checkout.checkout("a") == -1

    # Single SKUs
    assert checkout.checkout("A") == 50
    assert checkout.checkout("B") == 30
    assert checkout.checkout("C") == 20
    assert checkout.checkout("D") == 15

    # Multiples
    assert checkout.checkout("ABCD") == 115
    assert checkout.checkout("CC") == 40
    # With offers
    assert checkout.checkout("AAABB") == 175

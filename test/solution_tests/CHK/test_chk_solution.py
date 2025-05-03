from lib.solutions.CHK.checkout_solution import CheckoutSolution


def test_checkout_solution():
    checkout = CheckoutSolution()

    assert checkout.checkout(None) == -1
    assert checkout.checkout("A") == 50
    assert checkout.checkout("B") == 30
    assert checkout.checkout("C") == 20
    assert checkout.checkout("D") == 15


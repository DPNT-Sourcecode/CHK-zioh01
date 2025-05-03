from collections import Counter
from typing import NamedTuple


class Offer(NamedTuple):
    "Model for offers."

    quantity: int
    price: int


class CheckoutSolution:
    def __init__(self):
        # Set the prices table for SKUs
        self.prices = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40}
        # Set the special offers for SKUs
        self.offers = {
            "A": [Offer(quantity=3, price=130), Offer(quantity=5, price=200)],
            "B": [Offer(quantity=2, price=45)],
        }
        # Set the offers with free items
        self.free_item_offers = {}

    # skus = unicode string
    def checkout(self, skus: str) -> int:
        # handle incorrect type for SKUs input
        if not isinstance(skus, str):
            return -1

        # handle invalid SKUs
        if any(item not in self.prices for item in skus):
            return -1

        # get counts for SKUs
        counts = Counter(skus)
        total = 0

        # determine the total checkout value (with offers applied)
        for item, count in counts.items():
            # handle items with applicable offers
            if item in self.offers:
                offer = self.offers[item]
                total += (count // offer.quantity) * offer.price
                total += (count % offer.quantity) * self.prices[item]
            else:
                total += count * self.prices[item]

        return total



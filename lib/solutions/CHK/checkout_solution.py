from collections import Counter
from typing import NamedTuple


class Offer(NamedTuple):
    "Model for offers."

    quantity: int
    price: int


class BuyXGetYFree(NamedTuple):
    buy_quantity: int
    free_item: str


class CheckoutSolution:
    def __init__(self):
        # Set the prices table for SKUs
        self.prices = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40}
        # Set the special offers for SKUs
        self.offers = {
            "A": [Offer(quantity=5, price=200), Offer(quantity=3, price=130)],
            "B": [Offer(quantity=2, price=45)],
        }
        # Set the offers with free items
        self.free_item_offers = {"E": BuyXGetYFree(buy_quantity=2, free_item="B")}

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

        # Apply free item offers first
        for item, offer in self.free_item_offers.items():
            if item in counts and offer.free_item in counts:
                free_count = counts[item] // offer.buy_quantity
                counts[offer.free_item] = max(0, counts[offer.free_item] - free_count)

        total = 0

        # determine the total checkout value (with offers applied)
        for item, count in counts.items():
            if item in self.offers:
                # Apply offers in order (best deals first)
                remaining = count
                for offer in self.offers[item]:
                    if remaining >= offer.quantity:
                        total += (remaining // offer.quantity) * offer.price
                        remaining %= offer.quantity

                # Add remaining items at regular price
                total += remaining * self.prices[item]
            else:
                total += count * self.prices[item]

        return total


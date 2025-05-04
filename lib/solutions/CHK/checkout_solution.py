from collections import Counter
from typing import NamedTuple


class Offer(NamedTuple):
    """Represents a multi-item price offer (e.g., 3A for 130)."""

    quantity: int  # Number of items needed for the offer
    price: int  # Special price when buying this quantity


class BuyXGetYFree(NamedTuple):
    """Represents a 'buy X get Y free' type of offer."""

    buy_quantity: int  # Number of items to buy
    free_item: str  # Item that is given for free


class CheckoutSolution:
    """Checkout system that calculates total price with various types of offers.

    This class implements a flexible pricing engine for a supermarket checkout system that
    handles multiple types of price offers for a variety of products (SKUs A through Z):

    1. Multi-item price offers (e.g., 3A for 130, 5A for 200, 10H for 80)
    2. 'Buy X get Y free' offers (e.g., buy 2E get 1B free, buy 3R get 1Q free)
    3. 'Buy X get X free' offers (e.g., buy 2F get 1F free, buy 3U get 1U free)

    The system always favors the customer when applying offers, applying offers with
    better value first and ensuring the customer gets the maximum possible discount.
    When multiple offers are available for the same item, larger offers are applied first
    as they provide better value.

    Methods:
        checkout(skus: str) -> int:
            Calculate the total price for a basket of items

    Example:
        >>> solution = CheckoutSolution()
        >>> solution.checkout("AABCD")
        # 2A = 100, B = 30, C = 20, D = 15, total = 165
        165
        >>> solution.checkout("AAABCD")
        # 3A offer = 130, B = 30, C = 20, D = 15, total = 195
        195
        >>> solution.checkout("EEB")
        # 2E = 80, B is free from the offer, total = 80
        80
        >>> solution.checkout("FFF")
        # 3F where one is free from the offer, total = 20
        20
        >>> solution.checkout("UUUU")
        # 3U = 120, 1U free, total = 120
        120
    """

    def __init__(self):
        # Base prices for each item
        self.prices = {
            "A": 50,
            "B": 30,
            "C": 20,
            "D": 15,
            "E": 40,
            "F": 10,
            "G": 20,
            "H": 10,
            "I": 35,
            "J": 60,
            "K": 80,
            "L": 90,
            "M": 15,
            "N": 40,
            "O": 10,
            "P": 50,
            "Q": 30,
            "R": 50,
            "S": 30,
            "T": 20,
            "U": 40,
            "V": 50,
            "W": 20,
            "X": 90,
            "Y": 10,
            "Z": 50,
        }

        # Multi-price offers for bulk purchases
        # Ordered by size for better customer value (larger offers first)
        self.multi_price_offers = {
            "A": [
                Offer(quantity=5, price=200),  # 5A for 200 (better value)
                Offer(quantity=3, price=130),  # 3A for 130
            ],
            "B": [Offer(quantity=2, price=45)],  # 2B for 45
            "H": [
                Offer(quantity=10, price=80),  # 10H for 80
                Offer(quantity=5, price=45),  # 5H for 45
            ],
            "K": [Offer(quantity=2, price=150)],  # 2K for 150
            "P": [Offer(quantity=5, price=200)],  # 5P for 200
            "Q": [Offer(quantity=3, price=80)],  # 3Q for 80
            "V": [
                Offer(quantity=3, price=130),  # 3V for 130
                Offer(quantity=2, price=90),  # 2V for 90
            ],
        }

        # Buy X get Y free offers
        self.free_item_offers = {
            "E": BuyXGetYFree(buy_quantity=2, free_item="B"),  # Buy 2E get 1B free
            "F": BuyXGetYFree(buy_quantity=2, free_item="F"),  # Buy 2F get 1F free
            "N": BuyXGetYFree(buy_quantity=3, free_item="M"),  # Buy 3N get 1M free
            "R": BuyXGetYFree(buy_quantity=3, free_item="Q"),  # Buy 3R get 1Q free
            "U": BuyXGetYFree(buy_quantity=3, free_item="U"),  # Buy 3U get 1U free
        }

    def _apply_free_item_offers(self, counts: Counter) -> Counter:
        """Apply 'buy X get Y free' offers and return adjusted counts.

        For offers like "Buy 2E get 1B free", this calculates how many B items
        can be claimed for free based on the number of E items in the basket.

        For offers like "Buy 2F get 1F free", this effectively means every third F is free.

        Args:
            counts: Counter of items in the basket

        Returns:
            Counter with adjusted item counts after applying free item offers
        """
        # Create a copy of the counts to avoid modifying the original
        adjusted_counts = counts.copy()

        # First, collect all the free items possible
        free_item_counts = Counter()
        for item, offer in self.free_item_offers.items():
            if item in counts:
                # Calculate how many free items can be claimed
                free_items = counts[item] // offer.buy_quantity
                if free_items > 0:
                    free_item_counts[offer.free_item] += free_items

        # Then, apply the adjustments for each free item
        for item, count in free_item_counts.items():
            if item in counts:
                # Don't give more free items than actually exist in the basket
                free_count = min(count, counts[item])

                # Special case for items that give themselves for free
                if any(
                    offer.free_item == item
                    and offer.buy_quantity * free_count <= counts[item]
                    for offer_item, offer in self.free_item_offers.items()
                    if offer_item == item
                ):
                    # For buy X get X free offers, we need a different calculation
                    # to avoid double counting
                    item_offers = [
                        (offer_item, offer)
                        for offer_item, offer in self.free_item_offers.items()
                        if offer_item == item and offer.free_item == item
                    ]
                    if item_offers:
                        offer_item, offer = item_offers[0]
                        # Calculate how many items are effectively free
                        # e.g., for 2F get 1F free, with 6F, 2 are free (every third item)
                        buy_quantity = offer.buy_quantity
                        total_count = counts[item]
                        free_count = total_count // (buy_quantity + 1)
                        adjusted_counts[item] = total_count - free_count
                else:
                    # For other items, simply reduce the count
                    adjusted_counts[item] = counts[item] - free_count

        return adjusted_counts

    def checkout(self, skus: str) -> int:
        """Calculate total price of items, including all applicable special offers.

        The method processes the basket by:
        1. Validating the input
        2. Applying "buy X get Y free" offers
        3. Applying multi-item price offers

        Args:
            skus: A string containing the SKUs of all products in the basket
                 Each character represents one item (e.g., "AABCD" = 2 A's, 1 B, 1 C, 1 D)

        Returns:
            Total checkout value after applying all offers, or -1 for invalid input
        """
        # Handle invalid data types
        if not isinstance(skus, str):
            return -1

        # Empty basket costs nothing
        if not skus:
            return 0

        # Check for invalid SKUs (items not in our price list)
        if any(item not in self.prices for item in skus):
            return -1

        # Count items in the basket
        counts = Counter(skus)
        total = 0

        # Step 1: Apply any "buy X get Y free" offers
        adjusted_counts = self._apply_free_item_offers(counts)

        # Step 2: Calculate price for each item type
        for item in self.prices:
            # Skip items not in the basket
            if item not in counts:
                continue

            # For items that might be free, use the adjusted count after applying free item offers
            count = adjusted_counts[item]

            # Skip if count is 0 after adjustments
            if count == 0:
                continue

            # Apply multi-price offers if available for this item
            if item in self.multi_price_offers:
                remaining = count
                # Apply each offer in order (larger offers first for better value)
                for offer in self.multi_price_offers[item]:
                    if remaining >= offer.quantity:
                        # Apply offer as many times as possible
                        offers_applied = remaining // offer.quantity
                        total += offers_applied * offer.price
                        # Calculate remaining items after applying offers
                        remaining %= offer.quantity
                # Add remaining items at regular price
                total += remaining * self.prices[item]
            else:
                # No multi-price offers - charge regular price
                total += count * self.prices[item]

        return total



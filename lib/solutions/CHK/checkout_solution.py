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
    handles multiple types of price offers:

    1. Multi-item price offers (e.g., 3A for 130, 5A for 200)
    2. 'Buy X get Y free' offers (e.g., buy 2E get 1B free)

    The system always favors the customer when applying offers, applying offers with
    better value first and ensuring the customer gets the maximum possible discount.

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
    """

    def __init__(self):
        # Base prices for each item
        self.prices = {"A": 50, "B": 30, "C": 20, "D": 15, "E": 40}

        # Multi-price offers for bulk purchases
        # Ordered by size for better customer value (larger offers first)
        self.multi_price_offers = {
            "A": [
                Offer(quantity=5, price=200),  # 5A for 200 (better value)
                Offer(quantity=3, price=130),  # 3A for 130
            ],
            "B": [Offer(quantity=2, price=45)],  # 2B for 45
        }

        # Buy X get Y free offers
        self.free_item_offers = {
            "E": BuyXGetYFree(buy_quantity=2, free_item="B")  # Buy 2E get 1B free
        }

    def _apply_free_item_offers(self, counts: Counter) -> Counter:
        """Apply 'buy X get Y free' offers and return adjusted counts.

        For offers like "Buy 2E get 1B free", this calculates how many B items
        can be claimed for free based on the number of E items in the basket.

        Args:
            counts: Counter of items in the basket

        Returns:
            Counter with adjusted item counts after applying free item offers
        """
        # Create a copy of the counts to avoid modifying the original
        adjusted_counts = counts.copy()

        for item, offer in self.free_item_offers.items():
            if item in counts:
                # Calculate how many complete sets of the offer item we have
                # and therefore how many free items can be claimed
                free_items = counts[item] // offer.buy_quantity

                if free_items > 0 and offer.free_item in counts:
                    # Reduce the count of the free item, but not below 0
                    # This ensures we don't give more free items than exist in the basket
                    adjusted_counts[offer.free_item] = max(
                        0, counts[offer.free_item] - free_items
                    )

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

            # Start with the original count
            count = counts[item]

            # For items that might be free, use the adjusted count after applying free item offers
            if item in [offer.free_item for _, offer in self.free_item_offers.items()]:
                count = adjusted_counts[item]

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



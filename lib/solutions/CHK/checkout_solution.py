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


class GroupDiscount(NamedTuple):
    """Represents a group discount offer (e.g., any 3 of S,T,X,Y,Z for 45)."""

    items: frozenset  # Set of items eligible for the group discount
    quantity: int  # Number of items needed for the discount
    price: int  # Special price when buying this quantity


class CheckoutSolution:
    """Checkout system that calculates total price with various types of offers.

    This class implements a flexible pricing engine for a supermarket checkout system that
    handles multiple types of price offers for a variety of products (SKUs A through Z):

    1. Multi-item price offers (e.g., 3A for 130, 5A for 200, 10H for 80)
    2. 'Buy X get Y free' offers (e.g., buy 2E get 1B free, buy 3R get 1Q free)
    3. 'Buy X get X free' offers (e.g., buy 2F get 1F free, buy 3U get 1U free)
    4. Group discount offers (e.g., buy any 3 of S,T,X,Y,Z for 45)

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
        >>> solution.checkout("STX")
        # Group discount: 3 of S,T,X for 45, total = 45
        45
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
            "K": 70,  # Updated from 80 to 70
            "L": 90,
            "M": 15,
            "N": 40,
            "O": 10,
            "P": 50,
            "Q": 30,
            "R": 50,
            "S": 20,  # Updated from 30 to 20
            "T": 20,
            "U": 40,
            "V": 50,
            "W": 20,
            "X": 17,  # Updated from 90 to 17
            "Y": 20,  # Updated from 10 to 20
            "Z": 21,  # Updated from 50 to 21
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
            "K": [Offer(quantity=2, price=120)],  # 2K for 120 (updated from 150)
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

        # Group discount offers
        self.group_discounts = [
            GroupDiscount(
                items=frozenset(["S", "T", "X", "Y", "Z"]),
                quantity=3,
                price=45,
            ),  # Any 3 of S,T,X,Y,Z for 45
        ]

    def _apply_free_item_offers(self, counts: Counter) -> Counter:
        """Apply 'buy X get Y free' offers and return adjusted counts.

        For offers like "Buy 2E get 1B free", this calculates how many B items
        can be claimed for free based on the number of E items in the basket.

        For offers like "Buy 2F get 1F free", this effectively means every third F is free.
        This also handles cases where the free item isn't in the basket (no effect)
        and where multiple free item offers apply to the same basket.

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

    def _apply_group_discounts(self, counts: Counter) -> (Counter, int):
        """Apply group discount offers and return adjusted counts and additional cost.

        For offers like "Buy any 3 of S,T,X,Y,Z for 45", this method:
        1. Identifies eligible items in the basket
        2. Applies the offer as many times as possible
        3. Returns adjusted counts and the additional cost from group discounts

        The method prioritises higher priced items for the discount to maximise
        customer value, as per supermarket policy.

        Args:
            counts: Counter of items in the basket

        Returns:
            tuple: (adjusted_counts, group_discount_cost)
                - adjusted_counts: Counter with items after applying group discounts
                - group_discount_cost: Total cost from group discounts
        """
        # Create a copy to avoid modifying the original
        adjusted_counts = counts.copy()
        total_group_cost = 0

        # Process each group discount offer
        for discount in self.group_discounts:
            # Get all eligible items and their counts
            eligible_items = []
            for item in discount.items:
                if item in adjusted_counts and adjusted_counts[item] > 0:
                    eligible_items.append(
                        (item, self.prices[item], adjusted_counts[item])
                    )

            # Sort by price descending to maximise customer value
            # Higher priced items are included in the offer first
            eligible_items.sort(key=lambda x: x[1], reverse=True)

            # Apply the discount as many times as possible
            while True:
                items_for_offer = []
                total_count = 0

                # Try to collect enough items for one offer
                for item, _, count in eligible_items:
                    # Skip if this item is depleted
                    if adjusted_counts[item] <= 0:
                        continue

                    # Take as many as needed/available
                    items_needed = min(
                        adjusted_counts[item], discount.quantity - total_count
                    )
                    if items_needed > 0:
                        items_for_offer.append((item, items_needed))
                        total_count += items_needed

                    # If we have enough items, stop looking
                    if total_count >= discount.quantity:
                        break

                # If we couldn't collect enough items, we're done
                if total_count < discount.quantity:
                    break

                # Apply the discount
                for item, count in items_for_offer:
                    adjusted_counts[item] -= count

                # Add the cost of this group discount
                total_group_cost += discount.price

        return adjusted_counts, total_group_cost

    def checkout(self, skus: str) -> int:
        """Calculate total price of items, including all applicable special offers.

        The method processes the basket by:
        1. Validating the input
        2. Applying "buy X get Y free" offers
        3. Applying group discount offers
        4. Applying multi-item price offers

        The checkout process prioritises customer value by applying offers in the
        optimal order: free item offers first (to avoid paying for items that should
        be free), then group discounts (to maximize savings on higher-priced items),
        then multi-item pricing offers (larger quantity offers before smaller ones).

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

        # Step 2: Apply group discount offers
        adjusted_counts, group_discount_cost = self._apply_group_discounts(
            adjusted_counts
        )
        total += group_discount_cost

        # Step 3: Calculate price for each item type
        for item in self.prices:
            # Skip items not in the basket
            if item not in counts:
                continue

            # For items that might be free or part of group discounts,
            # use the adjusted count after applying those offers
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


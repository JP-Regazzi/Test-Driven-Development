class Checkout:
    def __init__(self):
        # Dictionary mapping article names to their prices.
        self.prices = {}
        # Dictionary mapping article names to their quantities in the basket.
        self.basket = {}
        # Dictionary mapping article names to discount rules: (min_qty, discount_rate)
        self.discount_rules = {}

    def set_price(self, article, price):
        """Assign a price to an article."""
        self.prices[article] = price

    def add_item(self, article):
        """Add an article to the basket.
        
        Raises:
            ValueError: If no price has been set for the article.
        """
        if article not in self.prices:
            raise ValueError(f"Price for article '{article}' is not set.")
        self.basket[article] = self.basket.get(article, 0) + 1

    def add_discount_rule(self, article, min_qty, discount_rate):
        """
        Add a discount rule for an article.
        
        Args:
            article (str): The name of the article.
            min_qty (int): The minimum quantity to trigger the discount.
            discount_rate (float): The discount rate (e.g., 0.10 for 10% off).
        """
        self.discount_rules[article] = (min_qty, discount_rate)

    def total(self):
        """Calculate the total price of the basket applying discount rules if applicable."""
        total_price = 0.0
        for article, quantity in self.basket.items():
            unit_price = self.prices.get(article, 0)
            # Check if a discount rule exists and if quantity qualifies.
            if article in self.discount_rules:
                min_qty, discount_rate = self.discount_rules[article]
                if quantity >= min_qty:
                    total_price += unit_price * quantity * (1 - discount_rate)
                else:
                    total_price += unit_price * quantity
            else:
                total_price += unit_price * quantity
        return total_price

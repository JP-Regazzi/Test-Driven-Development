# checkout.feature

Feature: Checkout process
  As an existing customer
  I want to manage my shopping basket
  So that I can add items, calculate totals, and receive discounts

  Scenario: Adding items and applying discount
    Given the price of "toothpaste" is 1.0
    And the price of "pinaple" is 0.5
    When I add "toothpaste" to the basket
    And I add "toothpaste" to the basket
    And I add "pinaple" to the basket
    And a discount rule for "toothpaste" is set with minimum quantity 2 and discount rate 0.10
    Then the total should be 2.3

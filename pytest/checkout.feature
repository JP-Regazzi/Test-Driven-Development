# checkout.feature

Feature: Checkout process
  As an existing customer
  I want to manage my shopping basket
  So that I can add items, calculate totals, and receive discounts

  Scenario: Adding items and applying discount
    Given the price of "apple" is 1.0
    And the price of "banana" is 0.5
    When I add "apple" to the basket
    And I add "apple" to the basket
    And I add "banana" to the basket
    And a discount rule for "apple" is set with minimum quantity 2 and discount rate 0.10
    Then the total should be 2.3

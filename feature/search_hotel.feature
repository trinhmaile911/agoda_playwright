Feature: Agoda Hotel Search

  @happy_path
  Scenario: Successful search for hotel
    Given I navigate to Agoda home page
    When I search for "Tokyo" as destination
    And I select check-in date 60 days from now
    And I select check-out date 65 days from now
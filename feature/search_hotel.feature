Feature: Agoda Hotel Search

  @happy_path
  Scenario: Successful search for hotel
    Given I navigate to Agoda home page
    When I search for "Tokyo" as destination
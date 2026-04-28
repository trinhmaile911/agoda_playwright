Feature: Agoda Hotel Search

  @happy_path
  Scenario: Successful search for hotel
    Given I navigate to Agoda home page
    When I search for "Tokyo" as destination
    And I select check-in date 60 days from now
    And I select check-out date 75 days from now
    And I set rooms to 4
    And I set rooms to 1
    And I set adults to 5
    And I set adults to 2
    And I set children to 0
    And I set children to 1
    And I click on the search button
    Then more than 0 properties are found

  @happy_path
  Scenario: Select budget per night
    Given I navigate to Agoda home page
    When I search for "Tokyo" as destination
    And I select check-in date 60 days from now
    And I select check-out date 75 days from now
    And I click on the search button
    And I select minimum budget to 20 percent and maximum budget percent to 30
    Then the budget slider should be set correctly

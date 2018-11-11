Feature: viewing a page of translations

  Scenario: Getting the translation page
    Given I have a test application
     When I visit "/"
     Then I get http status "200"

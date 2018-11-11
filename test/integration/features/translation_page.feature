Feature: viewing a page of translations

  Scenario: Getting the translation page
    Given I have a test application
     When I visit "/translations"
     Then I get http status "200"

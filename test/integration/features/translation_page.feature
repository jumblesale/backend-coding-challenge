Feature: viewing a page of translations

  Scenario: Getting the translation page
    Given I have a test application
     When I visit "/"
     Then I get http status "200"


  Scenario: Submitting a new translation
    Given I have a test application
      And I have data with "text" set to "translate me"
     When I "post" that data to "/"
     Then I get http status "200"
Feature: Requesting a new translation in sandbox

  Scenario: Creating a translation
    Given I have a dev application
     When I request a new translation
     Then I can see that translation

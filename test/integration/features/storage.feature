Feature: Storing and retrieving uids

  Scenario: Saving and then retrieving a uid
    Given I have a storage adapter
      And I create a new translation with uid "123abc"
      And I create a new translation with uid "789xyz"
     When I retrieve all saved translations
     Then I get uid "123abc"
      And I get uid "123abc"

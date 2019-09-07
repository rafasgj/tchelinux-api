Feature: Manage users and authentication.

Scenario: Create a new user
    Given an unregistered user name "The User" and email "theuser@tchelinux.org"
        And the user password "1234"
    When I create a new account
    Then there is 1 item in the table users

Scenario: Authenticate user
    Given there are registered users
        | name     | email                 | password |
        | The User | theuser@tchelinux.org | 1234     |
    When the user "theuser@tchelinux.org" logs in with password "1234"
    Then the operation succeeds
        And authentication code is generated

Scenario: Failed authentication
    Given there are registered users
        | name     | email                 | password |
        | The User | theuser@tchelinux.org | 1234     |
    When the user "theuser@tchelinux.org" logs in with password "7654"
    Then the operation exits with code 400

Scenario: Terminate session of an authenticated user
    Given the user "theuser@tchelinux.org" has authenticated in the system
    When the user ends its session
    Then the operation succeeds

Scenario: Terminate session of a non-authenticated user
    When the user ends its session
    Then the operation exits with code 401

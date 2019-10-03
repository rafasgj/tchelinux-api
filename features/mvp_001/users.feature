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
    Then the operation exits with code 401

Scenario: Terminate session of an authenticated user
    Given the user has no administrator priviledges
    When the user ends its session
    Then the operation succeeds

Scenario: Terminate session of a non-authenticated user
    When the user ends its session
    Then the operation exits with code 401

Scenario: User try to access restricted services after logout
    Given the user has administrator priviledges
        And the user ends its session
    When I add a city with the JSON data
        """
        {"name": "Porto Alegre", "cname": "poa"}
        """
    Then the operation exits with code 401

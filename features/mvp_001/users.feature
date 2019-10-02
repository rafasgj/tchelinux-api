Feature: Manage users and authentication.

Scenario: Create a new user
    Given no user is registered
    When I register with
        | name     | email                 | password |
        | The User | theuser@tchelinux.org | 1234     |
    Then there is 1 item in the table users

Scenario: Authenticate user
    Given there are registered users
        | name     | email                 | password |
        | The User | theuser@tchelinux.org | 1234     |
    When I login with email "theuser@tchelinux.org" and password "1234"
    Then the operation succeeds
        And an authentication code is generated

Scenario: Failed authentication
    Given there are registered users
        | name     | email                 | password |
        | The User | theuser@tchelinux.org | 1234     |
    When I login with email "theuser@tchelinux.org" and password "4321"
    Then the operation exits with code 401

Scenario: Terminate session of an authenticated user
    Given the user "theuser@tchelinux.org" has authenticated in the system
    When the user ends its session
    Then the operation succeeds

Scenario: Terminate session of a non-authenticated user
    When the user ends its session
    Then the operation exits with code 401

Scenario: User try to access restricted services after logout
    Given the user "theuser@tchelinux.org" has authenticated in the system
        And the user ends its session
    When I add a city with the JSON data
        """
        {"name": "Porto Alegre", "cname": "poa"}
        """
    Then the operation exits with code 401

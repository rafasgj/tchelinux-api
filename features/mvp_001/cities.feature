Feature: Manage cities.
    As an administrator, I want to list all cities.
    As an administrator, I want to add a new city.
    As an administrator, I want to change a city name.

Scenario: Add city to a database, unauthenticated
    Given a database with no cities
    When I add the city "Porto Alegre" with cname "poa"
    Then the operation exits with code 401

Scenario: Add city to a database, authenticated as an user.
    Given a database with no cities
        And the user "theuser@tchelinux.org" has authenticated in the system
    When I add the city "Porto Alegre" with cname "poa"
    Then the operation exits with code 403

Scenario: Add city to a database, authenticated as an administrator.
    Given a database with no cities
        And the admin "theadmin@tchelinux.org" has authenticated in the system
    When I add the city "Porto Alegre" with cname "poa"
    Then the operation exits with code 201
        And there is 1 item in the table cities

Scenario: Add city to a database with JSON.
    Given a database with no cities
        And the admin "theadmin@tchelinux.org" has authenticated in the system
    When I add a city with the JSON data
        """
        {"name": "Porto Alegre", "cname": "poa"}
        """
    Then the operation exits with code 201
        And there is 1 item in the table cities

Scenario: List cities in a database with only one city.
    Given the city "Porto Alegre" with cname "poa" exists in the database
    When I want to list all cities in the database
    Then the resulting JSON is
        """
        [
        {"name": "Porto Alegre", "cname": "poa"}
        ]
        """

Scenario: List cities in a database with more than one city.
    Given the city "Porto Alegre" with cname "poa" exists in the database
        And the city "Novo Hamburgo" with cname "nh" exists in the database
    When I want to list all cities in the database
    Then the resulting JSON is
        """
        [
            {"name": "Porto Alegre", "cname": "poa"},
            {"name": "Novo Hamburgo", "cname": "nh"}
        ]
        """

Feature: Manage cities.
    As an administrator, I want to list all cities.
    As an administrator, I want to add a new city.
    As an administrator, I want to change a city name.

Scenario: Add city to a database.
    Given a database with no cities
    When I add the city "Porto Alegre" with cname "poa"
    Then there is 1 item in the table cities

Scenario: Add city to a database with JSON.
    Given a database with no cities
    When I add a city with the JSON data
        """
        {"name": "Porto Alegre", "cname": "poa"}
        """
    Then there is 1 item in the table cities

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

Feature: Manage institutions.
    As an administrator, I want to list all institutions of a city.

Scenario: Add an institution to a database.
    Given the city "Porto Alegre" with cname "poa" exists in the database
        And no institution exists
        And the user has administrator priviledges
    When I add the institution
        """
        {
            "nick": "tchelinuxu",
            "name": "Universidade Tchelinux",
            "address": "R. Livre, 1234",
            "city": "poa",
            "latitude": -30.0281574,
            "longitude": -51.2308308
        }
        """
    Then there is 1 item in the table institutions

Scenario: Add an institution to a database, from JSON data.
    Given the city "Porto Alegre" with cname "poa" exists in the database
        And no institution exists
        And the user has administrator priviledges
    When I add the institution from JSON data
        """
        {
            "nick": "tchelinuxu",
            "name": "Universidade Tchelinux",
            "address": "R. Livre, 1234",
            "city": "poa",
            "latitude": -30.0281574,
            "longitude": -51.2308308
        }
        """
    Then there is 1 item in the table institutions

Scenario: List institutions in a city, by city code.
    Given the city "Porto Alegre" with cname "poa" exists in the database
        And an institution exists in the database
            """
            {
                "nick": "tchelinuxu",
                "name": "Universidade Tchelinux",
                "address": "R. Livre, 1234",
                "city": "poa",
                "latitude": -30.0281574,
                "longitude": -51.2308308
            }
            """
    When I want to list all institutions in the city "poa"
    Then the resulting JSON is
        """
        [{
            "nick": "tchelinuxu",
            "name": "Universidade Tchelinux",
            "address": "R. Livre, 1234",
            "city": "poa",
            "latitude": -30.0281574,
            "longitude": -51.2308308
        }]
        """

Scenario: List institutions in a city, by city name.
    Given the city "Porto Alegre" with cname "poa" exists in the database
        And an institution exists in the database
            """
            {
                "nick": "tchelinuxu",
                "name": "Universidade Tchelinux",
                "address": "R. Livre, 1234",
                "city": "poa",
                "latitude": -30.0281574,
                "longitude": -51.2308308
            }
            """
    When I want to list all institutions in the city "Porto Alegre"
    Then the resulting JSON is
        """
        [{
            "nick": "tchelinuxu",
            "name": "Universidade Tchelinux",
            "address": "R. Livre, 1234",
            "city": "poa",
            "latitude": -30.0281574,
            "longitude": -51.2308308
        }]
        """

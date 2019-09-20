Feature: List eventos.
    As an administrator, I want to create a new event.
    As a participant, I want to know which are the next events.
    As a participant, I want to know which are the next events close to my city.
    As a participant, I want to know which events occur near my city.
    As a participant, I want to know the details of a specific event.

Scenario: Add an event to the database.
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
    When I create an event for "tchelinuxu", 120 days from now
    Then there is 1 item in the table events

Scenario: List next event.
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
        And the city "Novo Hamburgo" with cname "nh" exists in the database
        And an institution exists in the database
            """
            {
                "nick": "opensource",
                "name": "Faculdades Open Source",
                "address": "AV. Aberta, 765",
                "city": "nh",
                "latitude": -29.6947027,
                "longitude": -51.11821
            }
            """
        And there is an event for "tchelinuxu", 40 days from now
        And there is an event for "opensource", 60 days from now
    When I ask for the next event
    Then with a date 40 days in the future, the resulting JSON is
        """
        {
            "cname": "poa",
            "city": "Porto Alegre",
            "institution": {
                "name": "Universidade Tchelinux",
                "address": "R. Livre, 1234",
                "latitude": -30.0281574,
                "longitude": -51.2308308
            },
            "rooms": [
                { "number": "1", "topic": "Room 1"},
                { "number": "2", "topic": "Room 2"},
                { "number": "3", "topic": "Room 3"}
            ]
        }
        """

Scenario: List next events.
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
        And there is an event for "tchelinuxu", 120 days from now
    When I ask for future events
    Then with a date 120 days in the future, the resulting JSON is
        """
        [{
            "cname": "poa",
            "city": "Porto Alegre",
            "institution": {
                "name": "Universidade Tchelinux",
                "address": "R. Livre, 1234",
                "latitude": -30.0281574,
                "longitude": -51.2308308
            },
            "rooms": [
                { "number": "1", "topic": "Room 1"},
                { "number": "2", "topic": "Room 2"},
                { "number": "3", "topic": "Room 3"}
            ]
        }]
        """

Scenario: List next event, in a specific city.
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
        And the city "Novo Hamburgo" with cname "nh" exists in the database
        And an institution exists in the database
            """
            {
                "nick": "opensource",
                "name": "Faculdades Open Source",
                "address": "Av. Aberta, 765",
                "city": "nh",
                "latitude": -29.6947027,
                "longitude": -51.11821
            }
            """
        And there is an event for "tchelinuxu", 40 days from now
        And there is an event for "opensource", 60 days from now
    When I ask for the next event in the city "Novo Hamburgo"
    Then with a date 60 days in the future, the resulting JSON is
        """
        {
            "cname": "nh",
            "city": "Novo Hamburgo",
            "institution": {
                "name": "Faculdades Open Source",
                "address": "Av. Aberta, 765",
                "latitude": -29.6947027,
                "longitude": -51.11821
            },
            "rooms": [
                { "number": "1", "topic": "Room 1"},
                { "number": "2", "topic": "Room 2"},
                { "number": "3", "topic": "Room 3"}
            ]
        }
        """

Scenario: List next event, in a specific city.
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
        And the city "Novo Hamburgo" with cname "nh" exists in the database
        And an institution exists in the database
            """
            {
                "nick": "opensource",
                "name": "Faculdades Open Source",
                "address": "Av. Aberta, 765",
                "city": "nh",
                "latitude": -29.6947027,
                "longitude": -51.11821
            }
            """
        And there is an event for "tchelinuxu", 40 days from now
        And there is an event for "opensource", 60 days from now
    When I ask for the next event 15 km closer to -29.7616438,-51.1514848
    Then with a date 60 days in the future, the resulting JSON is
        """
        [{
            "cname": "nh",
            "city": "Novo Hamburgo",
            "institution": {
                "name": "Faculdades Open Source",
                "address": "Av. Aberta, 765",
                "latitude": -29.6947027,
                "longitude": -51.11821
            },
            "rooms": [
                { "number": "1", "topic": "Room 1"},
                { "number": "2", "topic": "Room 2"},
                { "number": "3", "topic": "Room 3"}
            ]
        }]
        """


Scenario: List next events, returning multiple events.
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
        And the city "Novo Hamburgo" with cname "nh" exists in the database
        And an institution exists in the database
            """
            {
                "nick": "opensource",
                "name": "Faculdades Open Source",
                "address": "Av. Aberta, 765",
                "city": "nh",
                "latitude": -29.6947027,
                "longitude": -51.11821
            }
            """
        And there is an event for "tchelinuxu", 15 days from now
        And there is an event for "opensource", 45 days from now
    When I ask for future events
    Then the answer has 2 events due in [15, 45] days with
        """
        [{
            "cname": "poa",
            "city": "Porto Alegre",
            "institution": {
                "name": "Universidade Tchelinux",
                "address": "R. Livre, 1234",
                "latitude": -30.0281574,
                "longitude": -51.2308308
            },
            "rooms": [
                { "number": "1", "topic": "Room 1"},
                { "number": "2", "topic": "Room 2"},
                { "number": "3", "topic": "Room 3"}
            ]
        },{
            "cname": "nh",
            "city": "Novo Hamburgo",
            "institution": {
                "name": "Faculdades Open Source",
                "address": "Av. Aberta, 765",
                "latitude": -29.6947027,
                "longitude": -51.11821
            },
            "rooms": [
                { "number": "1", "topic": "Room 1"},
                { "number": "2", "topic": "Room 2"},
                { "number": "3", "topic": "Room 3"}
            ]
        }]
        """

Scenario: List next events, with some that has passed.
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
        And the city "Novo Hamburgo" with cname "nh" exists in the database
        And an institution exists in the database
            """
            {
                "nick": "opensource",
                "name": "Faculdades Open Source",
                "address": "Av. Aberta, 765",
                "city": "nh",
                "latitude": -29.6947027,
                "longitude": -51.11821
            }
            """
        And there is an event that occurred 15 days ago in "tchelinuxu"
        And there is an event for "opensource", 15 days from now
    When I ask for future events
    Then with a date 15 days in the future, the resulting JSON is
        """
        [{
            "cname": "nh",
            "city": "Novo Hamburgo",
            "institution": {
                "name": "Faculdades Open Source",
                "address": "Av. Aberta, 765",
                "latitude": -29.6947027,
                "longitude": -51.11821
            },
            "rooms": [
                { "number": "1", "topic": "Room 1"},
                { "number": "2", "topic": "Room 2"},
                { "number": "3", "topic": "Room 3"}
            ]
        }]
        """

Scenario: List next event.
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
        And there is an event for "tchelinuxu", 40 days from now
    When I configure the event rooms to
        | number | topic       |
        |  A321  | Development |
        |  A323  | SysAdmin    |
        |  A324  | Community   |
    Then there is an event for "tchelinuxu" that will occur in 40 days
        """
        {
            "cname": "poa",
            "city": "Porto Alegre",
            "institution": {
                "name": "Universidade Tchelinux",
                "address": "R. Livre, 1234",
                "latitude": -30.0281574,
                "longitude": -51.2308308
            },
            "rooms": [
                { "number": "A321", "topic": "Development"},
                { "number": "A323", "topic": "SysAdmin"},
                { "number": "A324", "topic": "Community"}
            ]
        }
        """
